const tools = require('./tools');
const { exit } = require('process');


require('dotenv').config()



if (!process.argv[2]) {
    console.log("---usage:     node scrape_images.js <path-to-photo-info-folder>")
    exit(1)
}


const puppeteer = require('puppeteer');

// open file stream 
const fs = require('fs');
const util = require('util');
const readdir = util.promisify(fs.readdir);
const makeDir = util.promisify(fs.mkdir);
const CHROME_PATH = Boolean(process.env.LINUX) ? process.env.CHROME_PATH : process.env.WINDOWS_CHROME_PATH

async function wait(ms) {
    return new Promise(resolve => {
        setTimeout(resolve, ms);
    });
}

function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Error classes 
class PageContactError extends Error {
    constructor(message) {
        super(message); // (1)
        this.name = "PageContactError"; // (2)
    }
}

function scrap_data_in_page_range(photo_info_path) {

    const json_path = photo_info_path.concat("/").concat(photo_info_path.split("Data/Images/")[1]).concat(".json")

    var photo_info = JSON.parse(fs.readFileSync(json_path));

    console.log(photo_info)


    puppeteer.launch({
        executablePath: CHROME_PATH,
        headless: false,
        userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1920,1080']
    }).then(async browser => {


        // create new page
        const page = await browser.newPage();

        // this does nothing atm
        for (var i = 0; i < photo_info.length; i++) {

            try {

                const property_id = photo_info[i]['id']


                // go to the appropriate base url + if necessary
                try {
                    await page.goto(photo_info[i]["link"], { waitUntil: 'networkidle2' });  // wait for no more than 2 network connections for 500ms    
                } catch (err) {
                    console.log("\n---------CONNECTED TO PAGE---------")

                }

                // check if login pages 
                try {
                    await page.$eval('#email', el => el.value = 'svercillo7@gmail.com');
                    await page.click("#formprop1submit")
                    await wait(200)
                } catch (err) {
                    // pass 
                }

                try {
                    await page.goto(photo_info[i]["link"], { waitUntil: 'networkidle2' });  // wait for no more than 2 network connections for 500ms    
                } catch (err) {
                    console.log(err)
                }

                console.log("clicking page")
                await page.evaluate(() => {
                    document.querySelector('.listing-slider-content-photo').click()
                });


                var page_data = await page.evaluate(() => {
                    return document.querySelector(
                        'div[class="modal-gallery-wrapper xs-gap-1 md-gap-2 md-p2 overflow-y-scroll outline-none"]'
                    ).innerHTML
                });




                const directory = photo_info_path.concat("/").concat(property_id)

                try {
                    await makeDir(directory); // create directory and proceed
                } catch (err) {
                    continue;
                }


                var arrayOfLines = page_data.match(/[^\r\n]+/g);

                var count = 0
                var page_data = []

                for (var i = 0; i < arrayOfLines.length; i++) {
                    let line = arrayOfLines[i]
                    if (line.startsWith("<figure")) {
                        if (count >= 10) {
                            break
                        }
                        count++;


                        var image_url = line.split('src="')[1].split('">')[0]
                        console.log(line)

                        var viewSource = await page.goto(image_url);
                        raw_photo_data = await viewSource.buffer(), function (err) {
                            if (err) {
                                console.log("error creating photo buffer ")
                                return console.log(err);
                            }
                        }

                        const image_id = uuidv4();
                        var photo_path = directory.concat("/").concat(image_id).concat(".png")

                        fs.writeFile(photo_path, raw_photo_data, (err) => {
                            if (err)
                                console.log(err)
                        });

                    }
                }

            } catch (err) {
                console.log("\n\nERROR:")
                console.log(err)
            }
        }

    }).catch(function (error) {
        console.log("\n\nerror\n")
        console.log(error)
    });

}


photo_info_path = process.argv[2]
scrap_data_in_page_range(photo_info_path)
