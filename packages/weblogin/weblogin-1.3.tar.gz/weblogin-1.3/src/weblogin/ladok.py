from lxml import html
from pprint import pprint
import requests
import weblogin
import weblogin.seamlessaccess as sa
import urllib.parse

class SSOlogin(weblogin.AutologinHandler):
  """
  Login handler (weblogin.AutologinHandler) for LADOK logins.
  """
  LOGIN_URL = "https://www.start.ladok.se/gui/loggain"
  
  def __init__(self,
      institution,
      vars=None,):
    """
    Creates a login handler that automates the LADOK part of authentication.

    - Requires `institution`. A string identifying the instutution at 
      SeamlessAccess.org.

    - An optional argument `vars` containing keys matching variables of the web 
      page forms whose values should be substituted for the values in the `vars` 
      dictionary. Note that the keys should be casefolded (lower case), since we 
      use `.casefold` to match variable names.
    """
    super().__init__()
    self.__institution = institution
    self.__logging_in = False
    self.__vars = vars or {}

  def need_login(self, response):
    """
    Checks a response to determine if logging in is needed,
    returns True if needed
    """
    if self.__logging_in:
      return False

    if response.status_code == requests.codes.unauthorized \
         and "ladok.se" in response.url:
      return True
    elif response.url.startswith(self.LOGIN_URL):
      return True

    return False


  def login(self, session, response, args=None, kwargs=None):
    """
    Performs a login based on the response `response` from a request to session 
    `session`.
    `args` and `kwargs` are the options from the request triggering the login 
    procedure, this is so that we can redo that request after logging in.

    Raises an AuthenticationError exception if authentication fails.
    """
    self.__logging_in = True
    response = session.get("https://www.start.ladok.se/Shibboleth.sso/Login"
                           "?target=https://www.start.ladok.se/gui/shiblogin")
    parsed_url = urllib.parse.urlparse(response.url, allow_fragments=False)
    if "seamlessaccess.org" not in parsed_url.netloc:
      raise weblogin.AuthenticationError(
                      f"seamlessaccess.org not in {parsed_url.netloc}")

    return_url = urllib.parse.unquote(
                            urllib.parse.parse_qs(parsed_url.query)["return"][0])
    if "{sha1}" in self.__institution:
      entityID = sa.get_entity_data_by_id(self.__institution)["entityID"]
    else:
      entityID = sa.find_entity_data_by_name(self.__institution)[0]["entityID"]
    if "?" in return_url:
      return_url += f"&entityID={entityID}"
    else:
      return_url += f"?entityID={entityID}"

    ladok_response = session.get(return_url)
    while "ladok.se" not in \
        urllib.parse.urlparse(ladok_response.url, allow_fragments=False).netloc:
      doc_tree = html.fromstring(ladok_response.text)
      try:
        form = doc_tree.xpath("//form")[0]
      except IndexError:
        raise AuthenticationError(f"Got page without any form and not on LADOK: "
                                  f"{ladok_response}")
      data = {}

      for var in form.xpath("//input"):
        if var.name:
          varname_casefold = var.name.casefold()
          if varname_casefold in self.__vars:
            data[var.name] = self.__vars[varname_casefold]
          else:
            data[var.name] = var.value or ""
      prev_url = ladok_response.url

      action_url = urllib.parse.urljoin(ladok_response.url, form.action)
      ladok_response = session.request(form.method, action_url, data=data)

      if ladok_response.url == prev_url:
        err = weblogin.AuthenticationError(f"infinite loop for "
                                           f"URL: {action_url}\n"
                                           f"data: {data}")
        err.variables = data
        raise err
    self.__logging_in = False

    if args and response.history:
      return session.request(*args, **kwargs)
    return ladok_response
