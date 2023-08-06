class InMemoryTokenProvider:

  def __init__(self, token: str):
    self._token = token

  def get_access_token(self):
    return self._token
