// EXCLUDES IMAGE DATA

const puppeteer = require('puppeteer');
const tools = require('./tools')

function scrap_data_starting_at_page(pageNum) {
    puppeteer.launch({
        executablePath: '/usr/bin/google-chrome-stable',
        headless: false,
        userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1920,1080']
    }).then(async browser => {



        function write_to_file(csvCols) {
            let string = "";
            for (var z = 0; z < csvCols.length; z++) {
                string += csvCols[z] + '\n';
            }

            fs.appendFile('../Data/data'.concat(pageNum).concat('.txt'), string, function (err) {
                if (err) throw err;
                console.log('Saved!');
            });
        }
        // create new page
        const page = await browser.newPage();

        // open file stream
        const fs = require('fs');

        const TOlong = -79.383186
        const TOlat = 43.653225

        // represents the num of cols before pushing to the csv file
        const MAXCOLS = 10;

        var csvCols = [];

        // this does nothing atm
        var endofentries = false;
        while (!endofentries) {
            // go to the appropriate base url + if necessary
            try {
                if (pageNum == 1) {
                    await page.goto("https://www.zolo.ca/toronto-real-estate/sold");
                } else {
                    await page.goto("https://www.zolo.ca/toronto-real-estate/sold/page-".concat(pageNum.toString(10)));
                }
                if (pageNum == 100) {
                    break
                }
            } catch (err) {
                throw new PageContactError("page num ".concat(pageNum).concat(" dose not exist"));
            }

            // get every link tag
            const urls = await page.$$eval('a', as => as.map(a => a.href));
            // set of used urls so we dont go the same place twice
            let used_urls = new Set();

            for (var i = 0; i < urls.length; i++) {
                // use the string in the split function as a delimeter for the url 
                var split = urls[i].split("https://www.zolo.ca/toronto-real-estate/");
                // if the url is a sold house
                if (split[1] != null) {
                    var firstChar = split[1][0];
                    // if link is a valid address...
                    if (!used_urls.has(urls[i]) && firstChar >= '0' && firstChar <= '9') {

                        console.log(urls[i]);

                        console.log(i)
                        used_urls.add(urls[i]);

                        try {
                            await page.goto(urls[i], { waitUntil: 'networkidle2' });  // wait for no more than 2 network connections for 500ms    
                        } catch (err) {
                            throw new PageContactError("page ".concat(urls[i]).concat(" either doesn't exist or there's a network connection error"));
                        }

                        // check if login pages 
                        try {
                            await page.$eval('#email', el => el.value = 'svercillo7@gmail.com');
                            await page.click("#formprop1submit")
                        } catch (er) {
                            // pass
                        }

                        try {
                            await page.goto(urls[i], { waitUntil: 'networkidle2' });  // wait for no more than 2 network connections for 500ms    
                        } catch (err) {
                            throw new PageContactError("page ".concat(urls[i]).concat(" either doesn't exist or there's a network connection error"));
                        }

                        let pagedata = await page.evaluate(() => {

                            const AMENITIES = [
                                "Groceries",
                                "Liquor Store",
                                "Restaurants",
                                "Coffee",
                                "Bank",
                                "Gas Station",
                                "Health & Fitness",
                                "Park",
                                "Library",
                                "Medical Care",
                                "Pharmacy",
                                "Mall",
                                "Movie Theatre",
                                "Bar"
                            ]

                            const VALUABLE_CAT = [
                                "List Date",
                                "Sold Date",
                                "Type",
                                "Style",
                                "Area",
                                "Municipality",
                                "Community",
                                "List Price",
                                "Bedrooms",
                                "Bathrooms",
                                "Kitchens",
                                "Rooms",
                                "Parking Total",
                                "Municipality District"
                            ]


                            try {
                                // create a set of known columns in the middle of the page, check to see nothing weird is coming up
                                const possibleColumns = new Set();
                                possibleColumns.add('Type');
                                possibleColumns.add('Style');
                                possibleColumns.add('Size');
                                possibleColumns.add('Lot Size');
                                possibleColumns.add('Age');
                                possibleColumns.add('Taxes');
                                possibleColumns.add('Walk Score');
                                possibleColumns.add('Pets');
                                possibleColumns.add('Days on Site');
                                possibleColumns.add('Maintenance Fees');
                                possibleColumns.add('Lease Term');
                                possibleColumns.add('Possession');
                                possibleColumns.add('All Inclusive');

                                // get all the spans
                                let spans = document.querySelectorAll('span[class="priv"]');

                                // if these conditions are true, page is not a SOLD property 
                                if (spans[5] == undefined || spans[5].innerText.localeCompare("Sold") != 0) {
                                    return -3;
                                }


                                let col_names = document.querySelectorAll('dt[class="column-label"]');

                                // skip Walk Score cause this is being weird
                                let temp = [];
                                for (var tt = 0; tt < col_names.length; tt++) {
                                    if (col_names[tt].innerText.localeCompare('Walk Score') != 0) {
                                        temp.push(col_names[tt]);
                                    }
                                }
                                col_names = temp;

                                // all of these are the same for each page
                                let address = document.querySelector('section>h1').innerText;
                                let bedNum = spans[0].innerText;
                                let bathNum = spans[1].innerText;
                                let sqarefootage = spans[2].innerText;
                                let sold_price = spans[3].innerText;
                                let soldOn = spans[6].innerText;


                                // init return
                                obj = {
                                    'sold_price': sold_price,
                                    'address': address,
                                    'bedNum': bedNum,
                                    'bathNum': bathNum,
                                    'sqarefootage': sqarefootage,
                                    'soldOn': soldOn,
                                }

                                var CATEGORIES = document.querySelectorAll('div[class="column-container column-break-inside-avoid"]')


                                for (var k = 0; k < CATEGORIES.length; k++) {
                                    var text_arr = CATEGORIES[k].innerText.split("\n")
                                    console.log(text_arr)
                                    for (var j = 1; j < text_arr.length; j += 3) {
                                        if (VALUABLE_CAT.includes(text_arr[j])) {
                                            obj[text_arr[j]] = text_arr[j + 1]
                                        }
                                    }

                                }

                                let divs = document.querySelectorAll('div[class="media-heading"]');

                                var amenities = []
                                for (var k = 0; k < divs.length; k++) {
                                    amenities.push(divs[k].innerText)
                                }

                                let sub_divs = document.querySelectorAll('div[class="media-sub-heading"]');

                                var dists = []
                                for (var k = 0; k < sub_divs.length; k++) {
                                    dists.push(sub_divs[k].innerText)
                                }

                                console.log(dists)
                                console.log(amenities)

                                var found_amenities_ind = {}
                                var count = 0
                                for (var j = 11; j < amenities.length; j += 4) {
                                    am = amenities[j]
                                    if (am.charAt(am.length - 2) == 'k' && am.charAt(am.length - 1) == 'm')
                                        am = am.substring(0, am.length - 2)

                                    am = am.replace(/[^A-Za-z\s]/g, '') // only keep letters in string
                                    am = am.trim()

                                    console.log(am)
                                    if (AMENITIES.includes(am)) {
                                        found_amenities_ind[count] = am
                                        obj[am.concat(" #1 name")] = amenities[j + 1]
                                        obj[am.concat(" #2 name")] = amenities[j + 2]
                                        obj[am.concat(" #3 name")] = amenities[j + 3]
                                    }
                                    count++
                                }


                                function get_entry(j, k) {
                                    var string = dists[parseInt(j) * 3 + 10 + k]

                                    var s_arr = string.split(" ")
                                    var distance = s_arr[s_arr.length - 2]

                                    if (string.charAt(string.length - 2) == 'k' && string.charAt(string.length - 1) == 'm')
                                        string = string.substring(0, string.length - 2)

                                    var address = string.replace(/[^A-Za-z\s]/g, '')
                                    address = s_arr[0].concat(address)
                                    address = address.replace("\n", "")
                                    address = address.substring(0, address.length - 4)
                                    distance = distance.replace("\n", "")
                                    return [address, distance]
                                }

                                for (var j in found_amenities_ind) {
                                    var am = found_amenities_ind[j]

                                    var first = get_entry(j, 0)
                                    var second = get_entry(j, 1)
                                    var third = get_entry(j, 2)
                                    obj[am.concat(" #1 address")] = first[0]
                                    obj[am.concat(" #2 address")] = second[0]
                                    obj[am.concat(" #3 address")] = third[0]

                                    obj[am.concat(" #1 distance")] = first[1]
                                    obj[am.concat(" #2 distance")] = second[1]
                                    obj[am.concat(" #3 distance")] = third[1]

                                }


                                console.log(obj)
                                return obj;
                            } catch (err) {
                                return -1
                            }
                        });
                        if (pagedata == -1 || pagedata == -2 || pagedata - 3) {
                            console.log(pagedata)
                            continue;
                        }

                        let str = pagedata['address'];
                        var j = 0;
                        for (; j < str.length; j++) {
                            if (str[j] == '-') {
                                break;
                            }
                        }
                        if (j != str.length) {
                            str = str.substring(j + 1);
                        }

                        pagedata['address'] = str;

                        // get coords from address
                        let coords = await tools.coords(pagedata['address']);

                        console.log(pagedata['address'])
                        console.log(coords)

                        if ('error' in coords ||
                            Math.abs(coords['lat'] - TOlat) > 5 ||
                            Math.abs(coords['lon'] - TOlong) > 5
                        ) {
                            console.log("geodata error");
                            continue;
                            // throw new BadRowError("geodata error");
                        }

                        pagedata['longitude'] = coords['lon'];
                        pagedata['latitude'] = coords['lat'];

                        pagedata['pageNum'] = pageNum;
                        pagedata['iterationNum'] = i;
                        pagedata['weblink'] = urls[i]
                        console.log(pagedata);


                        // convert json to string
                        pagedata = JSON.stringify(pagedata);

                        // save json object to data folder

                        csvCols.push(pagedata);

                        if (csvCols.length >= MAXCOLS) {
                            write_to_file(csvCols)
                            csvCols = [];
                        }

                    }
                }
            }
            pageNum++;
        }

    }).catch(function (error) {
        console.error(error);
    });
}

// Error classes 
class PageContactError extends Error {
    constructor(message) {
        super(message); // (1)
        this.name = "PageContactError"; // (2)
    }
}

class BadRowError extends Error {
    constructor(message) {
        super(message); // (1)
        this.name = "BadRowError"; // (2)
    }
}



scrap_data_starting_at_page(97)