# Copernic360

## Overwiew

[Copernic360][product] enables 6 degree-of-freedom (6DOF) motion in standard
360° VR content to allow users to move freely in scenes.  It consists of two
components: a Unity plugin; and a [Cloud API][apidoc].

Every piece of content is different, which is why the Copernic360 Unity plugin
requires configuration files with metadata for your content in order to enable
6DOF support. Copernic360 provides a [Cloud API][apidocs] to preprocess your
content, providing a configuration file that is used by the Unity plugin at
runtime.

## Command-line tool

The copernic360 command-line wraps [Kagenova][kagenova]'s Copernic360 [Cloud
API][apidocs].  In short, it allows users to post 360 images and videos and get
Copernic360 configuration files back.

Users first need an account with Kagenova's [Copernic360][product]. After
installing the tool via [pip][pip], users can interact with the Copernic360 API
as follows:

```bash
# get help
copernic360 --help
# check user login
copernic350 check-login
# check user's credits
copernic350 check-credit
# upload image.jpg and get its configution back (config.6dof)
copernic360 process-content image.jpg config.6dof
# list currently uploaded contents
copernic360 contents
```

See the command-line help for futher functionality and parameters.

[apidocs]: https://api.copernic360.ai/apidocs
[kagenova]: https://kagenova.com/
[product]: https://kagenova.com/products/copernic360/
[pip]: https://pip.pypa.io/en/stable/

Note that passwords and usernames can be either given on the command-line or in
the environment variables:

- `COPERNIC360_USER`
- `COPERNIC360_PASSWORD`