# uptimePage

**uptimePage** is an uptime monitoring tool for tracking the availability and performance of your Linux systems. It provides a user-friendly interface to monitor the status of multiple systems, ensuring that you're always aware of their uptime and potential downtimes.

## Features

- Monitor uptime for multiple Linux systems.
- User-friendly web interface for easy access.
- Customizable alerts for system downtime.
- Real-time statistics and performance tracking.
- Lightweight and easy to install.

## Server Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ha1fdan/uptimePage.git
   ```

2. Navigate to the project directory:

   ```bash
   cd uptimePage/server
   ```

3. Run the installation script:

   ```bash
   ./installServer.sh
   ```

### Usage

1. Start the uptimePage Server service:

   ```bash
   systemctl start uptimePageServer
   ```

2. Access the web interface at `http://localhost:8190` (or your desired port) to monitor your systems.

3. Add systems to monitor using the web interface or by editing the configuration file:

   ```bash
   nano config/systems.conf
   ```

4. Set up alert preferences for downtime notifications.

## Client Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ha1fdan/uptimePage.git
   ```

2. Navigate to the project directory:

   ```bash
   cd uptimePage/client
   ```

3. Run the installation script:

   ```bash
   ./installClient.sh
   ```


## Configuration

Edit the `config/settings.conf` file to customize settings such as:

- Monitoring intervals.
- Notification via Discord Webhooks.

## Contributing

We welcome contributions! If you want to contribute, please:

1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push to the branch.
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Feel free to customize this as needed!
