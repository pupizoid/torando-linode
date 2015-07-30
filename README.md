# Tornado-linode
Linode api client written on python, which is available to use in tornado framework

# Usage

```
class TestLinode(base.BaseHandler):
    @gen.coroutine
    def get(self):
        l = linode.LinodeCommand()
        r = yield l.execute('domain.list')
        self.write(json.dumps(r))
        self.finish()
```
# Todo

* command line option parser
* test
