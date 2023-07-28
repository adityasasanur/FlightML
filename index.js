const chromium = require('chrome-aws-lambda');
const puppeteer = chromium.puppeteer;
const puppeteer = require('puppeteer')
const fs = require("fs");
const csv = require("csv-parser");

exports.handler = async (event) => {
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);
  let day = tomorrow.getDate();
  let month = tomorrow.getMonth() + 1;
  let year = tomorrow.getFullYear();
  let currentDate = `${year}-${month}-${day}`;

  const links = [];
  fs.createReadStream("utils/flightLinks.csv")
    .pipe(csv())
    .on("data", (data) => {
      const rowValues = Object.values(data);
      links.push(rowValues[0]);
    });
  var ret = {};

  const executablePath = await chromium.executablePath;
  const browser = await puppeteer.launch({ args: chromium.args, executablePath });
  const page = await browser.newPage();

  for (let i = 0; i < 1; i++) {
    const link = links[i] + currentDate;
    console.log(link);

    for (let j = 0; j < 3; j++) {
      await page.goto(link);

      // Go through the flight options and try to click them
      try {
        await page.waitForSelector(".yR1fYc");
        const flights = await page.$$(".yR1fYc");
        flights[j].click();
      } catch (error) {
        console.log("Could not get to the link");
        continue;
      }

      // Get the data from each flight
      try {
        await page.waitForSelector(".ke9kZe-LkdAo-RbRzK-JNdkSc.pKrx3d");
        const prices = await page.$$eval(
          ".ke9kZe-LkdAo-RbRzK-JNdkSc.pKrx3d",
          (elements) => {
            return elements.map((element) => {
              x = element.getAttribute("aria-label");
              x = x.split(" ");
              return parseInt(x[x.length - 1].substring(1));
            });
          }
        );
        ret["prices"] = prices.reverse();
      } catch (error) {
        console.log(error);
        console.log("Could not get flight price history");
        continue;
      }

      try {
        // Find num stops
        const stopsWrapper = await page.$(".EfT7Ae.AdWm1c.tPgKwe");
        const stopsElement = await stopsWrapper.$(".ogfYpf");
        const stopsAttributeValue = await page.evaluate(
          (element) => element.getAttribute("aria-label"),
          stopsElement
        );
        const stops = stopsAttributeValue.split(" ")[0];
        const numStops = parseInt(stops) || 0;
        ret["stops"] = numStops;

        // PARSE DURATION (HOURS)
        const durationElement = await page.$(".gvkrdb.AdWm1c.tPgKwe.ogfYpf");
        const durationAttributeValue = await page.evaluate(
          (element) => element.getAttribute("aria-label"),
          durationElement
        );
        const duration = durationAttributeValue.split(" ");
        const duration_hours =
          parseInt(duration[2]) + parseInt(duration[4]) / 60;
        ret["duration"] = duration_hours;

        // GET DATE
        ret["year"] = year;
        ret["month"] = month;
        ret["day"] = day;
        ret["dow"] = tomorrow.getDay();

        // GET AIRLINE
        const airlineElement = await page.$(".sSHqwe.tPgKwe.ogfYpf span");
        const airlineInnerHTML = await page.evaluate(
          (element) => element.innerHTML,
          airlineElement
        );
        const airlineEncoding = require("./utils/airlineEncodings.json");
        const airline_int = airlineEncoding[airlineInnerHTML];
        ret["airline"] = airline_int;

        // GET DEPARTURE
        const departureTimeElement = await page.$x(
          '//span[@jscontroller="cNtv4b"]'
        );
        const departureTimeInnerHTML = await page.evaluate(
          (element) => element.innerHTML,
          departureTimeElement[0]
        );
        const departureTime = departureTimeInnerHTML.split("\u202f");
        const departureTime_hhmm = departureTime[0].split(":");
        const departureTime_float =
          parseFloat(departureTime_hhmm[1]) +
          12 * (departureTime[1].substring(0, 2) === "PM") +
          parseFloat(departureTime_hhmm[2]) / 60;
        ret["depart"] = departureTime_float;

        // GET DEPARTING/ARRIVING AIRPORT
        const departureAirportElement = await page.$x(
          '(//span[@jscontroller="cNtv4b"])[3]'
        );
        const departingAirportInnerHTML = await page.evaluate(
          (element) => element.innerHTML,
          departureAirportElement[0]
        );
        const arrivingAirportElement = await page.$x(
          '(//span[@jscontroller="cNtv4b"])[4]'
        );
        const arrivingAirportInnerHTML = await page.evaluate(
          (element) => element.innerHTML,
          arrivingAirportElement[0]
        );
        const airportEncoding = require("./utils/airportEncodings.json");
        const departure_airport_int =
          airportEncoding[departingAirportInnerHTML];
        const arriving_airport_int = airportEncoding[arrivingAirportInnerHTML];
        ret["depart_airport"] = departure_airport_int;
        ret["arrive_airport"] = arriving_airport_int;

        row = [
          ret.depart_airport,
          ret.arrive_airport,
          ret.depart,
          ret.airline,
          ret.year,
          ret.month,
          ret.day,
          ret.dow,
          ret.duration,
          ret.stops,
        ] + ret.prices;
        console.log(row)
      } catch (error) {
        console.log(error);
        console.log("Could not find data");
        continue;
      }

      // console.log(ret);
    }
  }
  await browser.close();
};
