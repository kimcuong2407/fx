// XAG=20 => đánh 0,01 thì 20point = 1$
// XAU=100 => đánh 0,01 thì 100point = 1$

// mặc định cứ 100 points = 1$ tất cả các cặp có giá trị 
const RateOneDollarEqualPoint = 100 / 100;

//dynamic
const firstTradeOrderType = 'sell';
const rr = 1.5;
const Money1RFirst = 30;
const points = 300;
const MoneyWinMinEachTrade = Money1RFirst * 1.2; // số tiền mà khi đóng all trade nhỏ nhất phải thắng được
const totalTrade = Math.round(10+ ((rr-1)*10));
// end dynamic
const fixedNumber = 2;
const lotFirstTrade = (Money1RFirst / points / RateOneDollarEqualPoint).toFixed(fixedNumber);

let volume = 1;
const orderTypeAndMoneyRR = [{
    'type': firstTradeOrderType,
    'lotSize': lotFirstTrade,
}, {
    'type': firstTradeOrderType == 'buy' ? 'sell' : 'buy',
    'lotSize': lotFirstTrade,
}];

// input1 : nhập vào số lệnh mà sẽ đạt tới TP
// logic
// vào lệnh Hedge nếu lệnh trước đó SL thì vào lệnh ngược chiều với lệnh trước đó với tỉ lệ RR: 1:3
// output: số tiền lãi
function totalRRWinAndLose(max) {
    let totalLot = 0;
    const results = [{
        type: firstTradeOrderType,
        sl: Money1RFirst,
        tp: Money1RFirst * rr,
        tradeNumber: 1,
        lot: lotFirstTrade,
    }];
    totalLot += parseFloat(lotFirstTrade);
    console.log(`Win trade so ${1}: ${calculateProfit(results)}`);

    for (let i = 2; i <= max; i++) {
        const lastResult = results[i - 2];
        let currentLotSize = lotFirstTrade;
        const orderType = lastResult.type == 'buy' ? 'sell' : 'buy';
        results.push({
            type: orderType,
            sl: Math.round(currentLotSize * points),
            tp: Math.round(currentLotSize * points) * rr,
            tradeNumber: i,
            lot: currentLotSize,
        });
        const totalAddedAfterTrade = i * 0.7 * Money1RFirst;
        while (calculateProfit(results) < MoneyWinMinEachTrade + (totalLot * 12) + totalAddedAfterTrade) {
            currentLotSize = (parseFloat(currentLotSize) + 0.01).toFixed(fixedNumber);
            results.pop()
            results.push({
                type: orderType,
                sl: Math.round(currentLotSize * points),
                tp: Math.round(currentLotSize * points) * rr,
                tradeNumber: i,
                lot: currentLotSize,
            });
        }

        totalLot += parseFloat(currentLotSize);
        console.log(`Win trade so ${i}: ${calculateProfit(results)} ---- total Lot: ${totalLot.toFixed(fixedNumber)}`);
    }

    const lotSize = results.map(i => i.lot).join('|');
    console.log(results);

    console.log('lotSize', lotSize);
    return calculateProfit(results);
}
totalRRWinAndLose(totalTrade);

function calculateProfit(results) {
    const typeProfit = results[results.length - 1].type;
    return results.reduce((acc, item) => {
        if (item.type == typeProfit) {
            acc += item.tp;
        } else {
            acc -= item.sl + item.tp;
        }
        return acc;
    }, 0)
}

console.log('rr: ', rr, 'point: ', points, 'moneyFirstTp', Money1RFirst);



