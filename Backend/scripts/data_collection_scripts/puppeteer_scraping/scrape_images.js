const tools = require('./tools');
const { exit } = require('process');


require('dotenv').config()



if (!process.argv[2] || !process.argv[3]){
    console.log("---usage:     node scrape_images.js 100 102    // will scrape pages 100-102 inclusive")
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

function scrap_data_in_page_range(pageNum, pageNumEnd, scrapingfunction){
    puppeteer.launch({ 
        executablePath: CHROME_PATH,
        headless: false,
        userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1920,1080'] 
        }).then(async browser => {
        
        
        // create new page
        const page = await browser.newPage();

        // this does nothing atm
        var endofentries = false;
        while( !endofentries){ 
            if (pageNum == pageNumEnd){
                break
            }

            // go to the appropriate base url + if necessary
            try{
                if (pageNum ==1){
                    await page.goto(
                        "https://www.zolo.ca/toronto-real-estate/sold", 
                        {waitUntil: 'networkidle2'}
                    );
                } else {
                    
                    await page.goto( 
                        "https://www.zolo.ca/toronto-real-estate/sold/page-".concat(pageNum.toString(10)), 
                        {waitUntil: 'networkidle2'}
                    );
                    
                }
            } catch (err){
                console.log(
                    "page num ".concat(pageNum).concat(" dose not exist")
                )
                throw new PageContactError("page num ".concat(pageNum).concat(" dose not exist"));
            }

            
            try {

                
                // get every link tag
                const urls = await page.$$eval('a', as => as.map(a => a.href));
                
                // set of used urls so we dont go the same place twice
                let used_urls = new Set();

                for ( var i =0; i<urls.length; i++){
                    try {

                        // use the string in the split function as a delimeter for the url 
                        var split = urls[i].split("https://www.zolo.ca/toronto-real-estate/"); 

                        // if the url is a sold house
                        if (split[1] != null){                           

                            var firstChar = split[1][0];
                            // if link is a valid address...
                            if ( !used_urls.has(urls[i]) && firstChar >= '0' && firstChar <='9'){    
                                
                                const link = urls[i]
                                console.log(urls[i]);
                                console.log(i)
                                used_urls.add(urls[i]);

                                try{
                                    await page.goto(urls[i], {waitUntil: 'networkidle2'});  // wait for no more than 2 network connections for 500ms    
                                } catch(err){
                                    console.log("\n---------CONNECTED TO PAGE---------")
                                    throw new PageContactError("page ".concat(urls[i]).concat(" either doesn't exist or there's a network connection error"));
                                }
                                
                                // check if login pages 
                                try { 
                                    await page.$eval('#email', el => el.value = 'svercillo7@gmail.com');
                                    await page.click("#formprop1submit")
                                    await wait(5000)
                                } catch (er) {
                                    // pass
                                }

                                try{
                                    await page.goto(urls[i], {waitUntil: 'networkidle2'});  // wait for no more than 2 network connections for 500ms    
                                } catch(err){
                                    throw new PageContactError("page ".concat(urls[i]).concat(" either doesn't exist or there's a network connection error"));
                                }

                                console.log("clicking page")
                                await page.evaluate(() => {
                                    document.querySelector('.listing-slider-content-photo').click()                            
                                });


                                var iteration = i
                                scrapingfunction(page, pageNum, i)

                                
                                var page_data = await page.evaluate(() => {
                                    return document.querySelector(
                                        'div[class="modal-gallery-wrapper xs-gap-1 md-gap-2 md-p2 overflow-y-scroll outline-none"]'
                                    ).innerHTML
                                });
                            
                                    

                                const address = await page.evaluate(() => {
                                    return document.querySelector('section>h1').innerText;
                                });

                                
                                var SKIP_PAGE = false
                                
                            
                                const directory1 = "../Data/Images/page_num_".concat(pageNum)
                            
                                try{
                                    await readdir(directory1)
                                    console.log('exiting...')
                                } catch (err){
                                    try{
                                        await makeDir(directory1); // create directory and proceed
                                    } catch(err){
                                        // pass
                                    }
                                    
                                }
                            
                                const directory2 = "../Data/Images/page_num_".concat(pageNum).concat("/iteration_").concat(iteration)
                            
                                try{
                                    await readdir(directory2)
                                    console.log('exiting...')
                                    SKIP_PAGE = true
                                } catch (err){
                                    try{
                                        await makeDir(directory2); // create directory and proceed
                                    } catch(err){
                                        // pass
                                    }
                                }

                                
                                if (!SKIP_PAGE){
                                    var arrayOfLines = page_data.match(/[^\r\n]+/g);
                            
                                    var c = 0
                                    var page_data = []
                        
                                    for (var i =0; i<arrayOfLines.length; i++){
                                        
                                        if (arrayOfLines[i].startsWith("<figure")){
                                            c ++
                                            console.log(arrayOfLines[i])
                                            
                                            if (c > 10){
                                                break
                                            }

                                            let image_link = (arrayOfLines[i].split('data-zoom-src="')[1]).split('">')[0];
                            
                                            let viewSource = await page.goto(image_link);
                            
                                            copy_address = "".concat(address)
                                            copy_address = copy_address.split(" ").join("_") // replace globally in the string 

                                            photo_data = await viewSource.buffer(), function (err) {
                                                if (err) {
                                                    console.log("error creating photo buffer ")
                                                    return console.log(err);
                                                }
                                            }
                                            
                                            
                                            local_photo_uri = "photo_num_".concat(c).concat(".png")
                                            
                                            fs.writeFile(  directory2.concat("/").concat(local_photo_uri), photo_data, (err) => {
                                                if (err)
                                                    console.log(err)
                                            });

                                            
                                            page_data.push(
                                                {
                                                    "page_num" : "".concat(pageNum),
                                                    "iteration" : "".concat(iteration),
                                                    "address" : address,
                                                    "link" : link,
                                                    "local_photo_uri" : local_photo_uri
                                                }
                                            )
                                            
                                        }

                                    }
                                        
                                    fs.writeFile(  directory2.concat("/").concat("photos_info.json"), JSON.stringify(page_data), (err) => {
                                        if (err)
                                            console.log(err)
                                    });

                                    console.log(page_data)
                                }
                            }
                        }
                    } catch (err){
                        console.log("\n\nerror\n")
                        console.log(err)
                        // pass 
                    }
                }

            } catch(err) {
                console.log("\n\nERROR\n")
                console.log(err)
            }
            pageNum ++;
        }

        await browser.close()
        
    }).catch(function(error) {
        console.log("\n\nerror\n")
        console.log(error)
    });

}


page_start = process.argv[2]
page_end = process.argv[3]

tools.scrap_data_in_page_range(page_start, page_end, scrape_all_images)
