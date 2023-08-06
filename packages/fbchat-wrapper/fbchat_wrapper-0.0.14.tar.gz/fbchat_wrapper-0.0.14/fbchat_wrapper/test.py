from py_fbchat import Client
for x in dir(Client):
    if x.startswith("on"):
        print(f"""def {x}(self,**kwargs):
    if "{x}" in self._event_list:
            self._event_list["{x}"](**kwargs)
        """)