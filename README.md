# nginx-proxy-manager

[NGINX Proxy Manager](https://nginxproxymanager.com/) easy configuration based on its [official documentation](https://nginxproxymanager.com/setup/).

For homepage serving documentation see also [NGINX Static Server](https://github.com/cupcakearmy/docker-static) project on Github.

## Usage

### Modify Docker Compose file

You can freely modify the [`docker-compose.yml`](docker-compose.yml) file according to your needs.

Here by commenting/uncommenting you can enable additional features as:

- dedicated Docker Network for you apps to avoid machine port exposition
- dedicated homepage to showcase all the apps you are serving along with their links

### Utility Homepage

You can enable an "easy to maintain" homepage with all the links to your exposed pages by uncommenting the `homepage` service in [`docker-compose.yml`](docker-compose.yml) file: this will add an NGINX server that serves only the [`hompage/index.html`](hompage/index.html) file.
>NOTE: **You'll need to configure a proxy host in your dashboard**.

By default this app is exposed on port 82 of your app, but you can modify the setting or even drop port exposition if your using the dedicated network: in this case inspect it and find the local IP given by Docker and use that with port 80 when configuring the proxy host in NPM dashboard.

Change the following lines in the final script of [`hompage/index.html`](hompage/index.html) according to your needs:

```javascript
const domain_or_ip = "<YOUR DOMAIN OR IP>";
const use_https = false;
const apps = [];
```

- `domain_or_ip`: insert the domain your're serving NPM from or the IP (private or public)
- `use_https`: boolean to indicate if ALL the apps are exposed via HTTP (false) or HTTPS (true)
- `apps`: insert the list of the exposed apps by subdomain. Hint: if you choose subdomains similar to your app names (e.g. with dash instead of spaces and all lower case) you can use the app names directly.

>NOTE: the `homepage` folder is mounted as a volume so you can change these settings in realtime without the need to turn down-up the Docker Network.

### Dedicated Network

It's possible to use an utility bash script [`external_network.sh`](external_network.sh) to turn on/off the entire Docker cluster choosing a dedicated Docker Network or the default one. Simply run:

```bash
./external_network.sh <enable|disable> <network-name>
```

- *enable*: creates a Docker network named after the chosen name runs NPM attached to it (along with the homepage if you uncommented the section)
- *disable*: turns off NPM, comments the "network" section in docker-compose.yml file and turns back NPM on
