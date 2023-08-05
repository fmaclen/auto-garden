# auto-garden

<p align="center"><img src="https://github.com/fmaclen/auto-garden/assets/1434675/8fc50981-174d-44af-89ae-b72e054ac3e9" width="192"/></p>

A self-learning project to get familiar with Python, electronics and gardening.

### Features

- Automatic irrigation
- Saves historical moisture readings and irrigation events to a database
- Web UI for monitoring the system

_As you can see, the web UI is very much a work in progress..._

![image](https://github.com/fmaclen/auto-garden/assets/1434675/c609872c-84b3-400e-bbe6-70eb5249782a)

The app relies on a database for the configuration of the **`plant pots`** you want to irrigate and the **`devices`** these `pots` are connected to. You can define all the settings for each pot (see table below) to determine when to irrigate and for how long. Every time the moisture reading changes it's automatically saved to the database.

### Tested on

- Rasperry Pi 4 Model B (`server` and/or `client`)
- Raspberry Pico W (`client` only)

---

## Getting started

### Raspberry Pi 4

#### Pi 4: Setup Server

1. Clone the repo: `git clone https://github.com/fmaclen/auto-garden.git`
2. Download and setup **PocketBase** (see [Development](#development) section)
3. Open port `8090` and `8888` on the device that's running the server and check the rule was added:

```bash
iptables -A INPUT -p tcp --dport 8888 -j ACCEPT
iptables -A INPUT -p tcp --dport 8090 -j ACCEPT
iptables -L INPUT
```

4. Create the `admin` account, `device` and `pots`:

| Pot Key               | Explanation                                                                                                           |
| --------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `id`                  | Identifier or ID associated with the pot                                                                              |
| `device`              | ID of the device which will control the pot                                                                           |
| `name`                | Name of the pot                                                                                                       |
| `moisture_low`        | The lower threshold % of moisture value below which the pot needs irrigation                                          |
| `moisture_high`       | The upper threshold % of moisture value above which the pot doesn't require irrigation                                |
| `moisture_sensor_dry` | The raw value the moisture sensor is reporting when it's exposed to the air                                           |
| `moisture_sensor_wet` | The raw value the moisture sensor is reporting when it's exposed to water                                             |
| `moisture_sensor_pin` | The GPIO pin number where the moisture sensor is connected. _Note: for Pi 4 the pin number refers to the ADC channel_ |
| `pump_max_attempts`   | The maximum number of pump attempts allowed per irrigation event                                                      |
| `pump_duration_in_s`  | The duration in seconds for which the pump remains on during irrigation                                               |
| `pump_frequency_in_s` | The duration in seconds to wait between pumps during an irrigation event                                              |
| `pump_relay_pin`      | The GPIO pin number number connected to the pump relay                                                                |

5. Run the **Web UI** server in another window:

```bash
python web/web.py
```

6. On another computer in the same network visit:

- `http://<your-local-ip-address>:8888` **(Web UI)**
- `http://<your-local-ip-address>:8090` **(PocketBase)**

7. In the **Web UI** configure the IP address of the **PocketBase** server, as well as the admin `username` and `password`. These values are saved locally on your browser.

#### Pi 4: Setup Client

1. Clone the repo: `git clone https://github.com/fmaclen/auto-garden.git` and `cd auto-garden`
2. Build the app with: `./script/build/pi_4`. This will generate `/dist/pi_4` folder with all the files.
3. Create a copy of `env.sample.py` and rename it to `dist/pi_4/env.py`. Update the file with the correct values.
4. Install the Python libraries `pip install -r dist/pi_4/requirements.txt`.

5. Start the app in another window:

```bash
python dist/pi_4/main.py
```

#### Pi 4: Client + Server in the same device

If you are running the `server` + `client` in a Pi 4, after following the setup steps above, you can start all 3 processes (in the background) with:

```bash
./scripts/start
```

Stop the server and app:

```bash
./scripts/stop
```

---

### Raspberry Pico W

#### Pico W: Setup Client

1. Clone the repo: `git clone https://github.com/fmaclen/auto-garden.git` and `cd auto-garden`
2. Build the app with: `./script/build/pico_w`. This will generate `/dist/pico_w` folder with all the files.
3. Create a copy of `env.sample.py` and rename it to `dist/pico_w/env.py`. Update the file with the correct values.
4. Copy the contents of the `dist/pico_w` folder to the Pico W's filesystem. If you are using **VSCode** I'd recommend using the [MicroPico](https://github.com/paulober/MicroPico/) extension, otherwise use [Thonny](https://thonny.org/).
5. Unplug from your computer and connect it to a power source. It should connect to the WiFi network set in `env.py` and start running the app. You can check if it's running by looking at the logged events in **PocketBase** or seeing the moisture readings in the **Web UI**.

---

## Development

1. Clone repo and install dependencies:

```bash
pip install -r requirements.txt
```

2. Download and unzip **Pocketbase** _(update the URL to match your OS architecture)_:

```bash
wget -O pocketbase.zip https://github.com/pocketbase/pocketbase/releases/download/v0.16.10/pocketbase_0.16.10_darwin_amd64.zip
unzip pocketbase.zip -d pocketbase
```

3. Start the database server in one window:

```bash
./pocketbase/pocketbase serve
```

4. Visit [http://127.0.0.1:8090](http://127.0.0.1:8090):

- Create an admin account
- Create a **Device** in the `devices` table
- Create a **Pot** in the `pots` table

5. Create a copy of `env.sample.py` and rename it to `env.py`. You can leave the default values for testing.

6. Run the tests. If you are using **VSCode** launch the debugger with the `Test: auto-garden` configuration (recommended). Alternatively, run the following command from the root of the project:

```bash
python -m pytest -s -v test/
```

---

### Hardware used

- Raspberry Pico W — [Amazon](https://www.amazon.com/Raspberry-Pico-Header-Pre-soldered-Headers/dp/B0BCFNX7KF?&_encoding=UTF8&tag=str1ct04st3r-20&linkCode=ur2&linkId=cdda9d5a8ca6995692981e911cece39c&camp=1789&creative=9325)
- Raspberry Pi 4 Model B 8GB — [Amazon](https://www.amazon.com/Raspberry-Pi-Computer-Suitable-Workstation/dp/B0899VXM8F/ref=sr_1_1?keywords=raspberry+pi+8gb&qid=1688998636&sr=8-1&ufe=app_do%253Aamzn1.fos.18ed3cb5-28d5-4975-8bc7-93deae8f9840&_encoding=UTF8&tag=str1ct04st3r-20&linkCode=ur2&linkId=a16c5297cc8d7943b6fc6e316b44c16d&camp=1789&creative=9325)
- [WayinTop](https://github.com/wayintop) Automatic Irrigation DIY Kit — [Amazon](https://www.amazon.com/gp/product/B07TMVNTDK/ref=ox_sc_act_title_1?smid=A22PZZC3JNHS9L&psc=1&_encoding=UTF8&tag=str1ct04st3r-20&linkCode=ur2&linkId=ce6d47f9b6c66d7ddfdfc58f7a0bfc32&camp=1789&creative=9325)
- CQRobot Ocean: ADS1115 16-Bit ADC - 4-Channel — [Amazon](https://www.amazon.com/gp/product/B08KFZ3PVT/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1&_encoding=UTF8&=str1ct04st3r-20&=ur2&=4cb6e0c4e9a39c09c126b68243484574&=1789&=9325)

