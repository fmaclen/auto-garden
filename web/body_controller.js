import PocketBase from "https://cdn.jsdelivr.net/npm/pocketbase@0.15.2/+esm";
import { Controller } from "https://unpkg.com/@hotwired/stimulus/dist/stimulus.js";
import { formatDistance } from "https://cdn.skypack.dev/date-fns@2.30.0/esm/index.js";
import "https://unpkg.com/chart.js@4.3.0/dist/chart.umd.js";

const SERVER_URL_KEY = "serverUrl";
const SERVER_USERNAME_KEY = "serverUsername";
const SERVER_PASSWORD_KEY = "serverPassword";

export default class BodyController extends Controller {
  static targets = [
    "pots",
    "potName",
    "potMoistureLevel",
    "potMoistureUpdated",
    "potIrrigationStatus",
    "potIrrigationPumps",
    "potIrrigationUpdated",
    "potLineChart",
    "notice",
    "serverUrl",
    "serverUsername",
    "serverPassword",
    "serverSubmit",
    "serverTime"
  ];

  async connect() {
    await this.connectToPocketBase();
    this.serverSubmitTarget.addEventListener(
      "click",
      async () => await this.setServerConfig()
    );

    this.loopId = setInterval(() => this.loop(), 1000);
  }

  async update() {
    const pots = await this.getPots();

    for (const [index, pot] of pots.items.entries()) {
      const moistures = await this.pb
        .collection("moistures")
        .getList(1, 500, {
          sort: "-updated",
          filter: `pot = '${pot.id}'`,
          expand: "pot",
        });
      const irrigations = await this.pb
        .collection("irrigations")
        .getList(1, 500, { sort: "-updated", filter: `pot = '${pot.id}'` });

      const labels = moistures.items
        .reverse()
        .map((moisture) => moisture.updated);

      const data = {
        labels: labels,
        datasets: [
          {
            label: "Moisture level",
            backgroundColor: "rgb(75, 192, 192)",
            borderColor: "rgb(75, 192, 192)",
            data: moistures.items.map((moisture) => moisture.level),
          }
        ],
      };

      const config = {
        type: "line",
        data: data,
        options: {
          animation: false,
          interaction: {
            mode: "index",
            intersect: false,
          },
          datasets: {
            line: {
              pointStyle: "circle",
              pointRadius: 0,
              pointHitRadius: 64,
              pointHoverBorderWidth: 1,
              borderWidth: 1.25,
              tension: 0.25,
            },
          },
          scales: {
            x: {
              ticks: {
                autoSkipPadding: 12,
                callback: (index) => {
                  return formatDistance(new Date(labels[index]), new Date(), {
                    addSuffix: true,
                  });
                },
              },
              grid: {
                drawBorder: false,
                tickLength: 0, // Removes an extra space between the chart and the axis labels
              },
            },
            y: {
              grace: "5%",
              ticks: {
                padding: 16,
                align: "center",
              },
              grid: {
                drawBorder: false,
                tickLength: 0, // Removes an extra space between the chart and the axis labels
                z: 1, // Make the zero line appear on top of chat data with a value of zero
                lineWidth: (context) => (context.tick.value == 0 ? 1 : 0), //Set only zero line visible
              },
            },
          },
        },
      };

      const lastestMoisture = moistures.items[moistures.items.length - 1]; // prettier-ignore
      this.potNameTargets[index].textContent = lastestMoisture.expand.pot.name; // prettier-ignore
      this.potMoistureLevelTargets[index].textContent = `${lastestMoisture.level}%`; // prettier-ignore
      this.potMoistureUpdatedTargets[index].setAttribute("datetime", new Date(lastestMoisture.updated).toISOString())
      
      const lastestIrrigation = irrigations.items[irrigations.items.length - 1]; // prettier-ignore
      if (lastestIrrigation) {
        this.potIrrigationStatusTargets[index].textContent = `${lastestIrrigation.status} /`; // prettier-ignore
        this.potIrrigationPumpsTargets[index].textContent = `${lastestIrrigation.pumps} pumps`; // prettier-ignore
        this.potIrrigationUpdatedTargets[index].setAttribute("datetime", new Date(lastestIrrigation.updated).toISOString())
      } else {
        this.potIrrigationStatusTargets[index].textContent = "Never irrigated";
      }

      const chartInstance = Chart.instances[index];

      // If the chart instance exists, update its config
      if (chartInstance) {
        chartInstance.config._config = config;
        chartInstance.update("none");
      } else {
        // Otherwise, create a new chart
        new Chart(this.potLineChartTargets[index], config);
      }
    }
  }

  async setServerConfig() {
    if (this.serverUrlTarget.value != "") localStorage.setItem(SERVER_URL_KEY, this.serverUrlTarget.value); // prettier-ignore
    if (this.serverUsernameTarget.value != "") localStorage.setItem(SERVER_USERNAME_KEY, this.serverUsernameTarget.value); // prettier-ignore
    if (this.serverPasswordTarget.value != "") localStorage.setItem(SERVER_PASSWORD_KEY, this.serverPasswordTarget.value); // prettier-ignore
    await this.connectToPocketBase();
  }

  async connectToPocketBase() {
    // Check if the localStorage has the server, username and password
    this.serverUrlTarget.value = localStorage.getItem(SERVER_URL_KEY);
    this.serverUsernameTarget.value = localStorage.getItem(SERVER_USERNAME_KEY);
    this.serverPasswordTarget.value = localStorage.getItem(SERVER_PASSWORD_KEY);

    if (
      !this.serverUrlTarget.value ||
      !this.serverUsernameTarget.value ||
      !this.serverPasswordTarget.value
    ) {
      this.noticeTarget.textContent = "Fill out all fields";
      this.noticeTarget.classList.remove("in-progress");
      this.noticeTarget.classList.add("negative");
      return;
    }

    try {
      this.pb = new PocketBase(this.serverUrlTarget.value);
      this.noticeTarget.classList.remove("negative");
      this.noticeTarget.classList.add("in-progress");
      this.noticeTarget.textContent = "Connecting...";

      await this.pb.admins.authWithPassword(
        this.serverUsernameTarget.value,
        this.serverPasswordTarget.value
      );
    } catch (error) {
      this.noticeTarget.textContent = error.message;
      this.noticeTarget.classList.remove("in-progress");
      this.noticeTarget.classList.add("negative");
      return;
    }

    this.noticeTarget.textContent = "Connected";
    this.noticeTarget.classList.remove("in-progress");
    this.noticeTarget.classList.add("positive");

    // Subscribe to changes in "moistures" and "irrigations"
    this.pb.collection("moistures").subscribe("*", () => this.update());
    this.pb.collection("irrigations").subscribe("*", () => this.update());

    // Adding the pot templates for each pot in the DB to the DOM
    if (this.potNameTargets.length === 0) {
      const pots = await this.getPots();
      for (const _ of pots.items) await this.setPotTemplate();
    }

    this.update();
  }

  async getPots() {
    return await this.pb.collection("pots").getList(1, 500);
  }

  async setPotTemplate() {
    const response = await fetch("pot.html");
    const html = new DOMParser().parseFromString(
      await response.text(),
      "text/html"
    ).body.firstChild;

    this.potsTarget.append(html);
  }

  removePotTemplates() {
    this.potsTarget.innerHTML = "";
  }
  
  loop() {
    this.serverTimeTarget.textContent = new Date().toLocaleString("en-US", {
      timeZone: "UTC",
      dateStyle: "full",
      timeStyle: "long",
    });

    [
      ...this.potMoistureUpdatedTargets,
      ...this.potIrrigationUpdatedTargets
    ].forEach((target) => {
      const lastUpdated = target.getAttribute("datetime");

      if(lastUpdated) {
        target.textContent = formatDistance(
          new Date(lastUpdated),
          new Date(),
          { addSuffix: true }
        );
      }
    });

    this.serverTimeTarget.textContent = new Date().toLocaleString("en-US", {
      timeZone: "UTC",
      dateStyle: "full",
      timeStyle: "long",
    });
  }

  async disconnect() {
    await this.pb.collection("moistures").unsubscribe();
    await this.pb.collection("irrigations").unsubscribe();
    this.removePotTemplates();
    clearInterval(this.loopId);
  }
}
