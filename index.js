const { getHistoricalRates } = require("dukascopy-node");
var fs = require('fs');
const dayjs = require('dayjs');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;


const pair = 'eurusd';
const timeframe = 'm15';
const startDate = '2020-01-01';
const endDate = dayjs();

const csvWriter = createCsvWriter({
  path: `download/${pair}-${timeframe}.csv`,
  header: [
    { id: 'timestamp', title: 'timestamp' },
    { id: 'open', title: 'open' },
    { id: 'high', title: 'high' },
    { id: 'low', title: 'low' },
    { id: 'close', title: 'close' },
    { id: 'volume', title: 'volume' },
  ]
});

(async () => {
  try {
    console.log('start')
    const data = await getHistoricalRates({
      instrument: pair,
      dates: {
        from: new Date(startDate),
        to: new Date(endDate),
      },
      timeframe: timeframe,
      format: "json",
    });
    console.log('done')
    const result = data.map(item => {
      item.timestamp = dayjs(item.timestamp).format('YYYY-MM-DD HH:mm:ss');
      return item;
    })
    console.log('start write file')

    csvWriter
      .writeRecords(result)
      .then(() => console.log('The CSV file was written successfully'));

    // console.log(data);
  } catch (error) {
    console.log("error", error);
  }
})();