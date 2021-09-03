const puppeteer = require('puppeteer');

// open file stream 
const fs = require('fs');
const util = require('util');
const { url } = require('inspector');
const writeFile = util.promisify(fs.writeFile);
const CHROME_PATH = Boolean(process.env.LINUX) ? process.env.CHROME_PATH : process.env.WINDOWS_CHROME_PATH


async function get_max_page_range(){
    puppeteer.launch({ 
        executablePath: CHROME_PATH,
        headless: false,
        userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1920,1080'] 
        }).then(async browser => {
        

        // create new page
        const page = await browser.newPage();
        
        await page.goto(
            "https://www.zolo.ca/toronto-real-estate/sold", 
            {waitUntil: 'networkidle2'}
        );

        const urls = await page.$$eval('a', as => as.map(a => a.href));
        
        max = -1
        for ( var i = urls.length-1; i>=0; i--){
            var url = urls[i]
            if (urls[i].includes("toronto-real-estate/sold/page-")){
                try{
                    var val = parseInt(url.split("toronto-real-estate/sold/page-")[1])
                    if (val > max){
                        max = val
                    }
                } catch (err){
                    // pass
                }
            }
        }

        if (max == -1){
            throw "Invalid URL"
        }


        const file_name = "../../Data/Images/page_ranges.txt"
        console.log("Creating file ".concat(file_name))
        await writeFile(file_name, "".concat(max), (err)=> {
            if (err)
                console.log(err)
        })

        await browser.close()
        

    }).catch(function(error) {
        console.error(error);
    });
}


get_max_page_range()
