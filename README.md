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
