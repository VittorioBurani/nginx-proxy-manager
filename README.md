# nginx-proxy-manager

NGINX Proxy Manager easy configuration based on its [official documentation](https://nginxproxymanager.com/setup/).

## Usage

### Modify Docker Compose file

You can freely modify the [`docker-compose.yml`](docker-compose.yml) file according to your needs.

### Use the utility script

It's also possible to use the utility bash script [`external_network.sh`](external_network.sh). The usage is:

```bash
./external_network.sh <enable|disable> <network-name>
```

- *enable*: creates a Docker network named after the chosen name and then runs NPM attached to it
- *disable*: turns off NPM, comments the "network" section in docker-compose.yml file and turns back NPM on

### Utility Custom Page

If you want to customize the default page to get a list of all the exposed proxied apps, you can simply copy the content of [`custompage.html`](custompage.html) in `Settings -> Default Site -> Custom` using the Dashboard.

Change the following lines in the final script according to your needs:

```javascript
const domain_or_ip = "<YOUR DOMAIN OR IP>";
const use_https = false;
const apps = [];
```

- `domain_or_ip`: insert the domain your're serving NPM from or the IP (private or public)
- `use_https`: boolean to indicate if ALL the apps are exposed via HTTP (false) or HTTPS (true)
- `apps`: insert the list of the exposed apps. The subdomain should be very similar to the app name: dash instead of spaces and all lower case.
