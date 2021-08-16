const puppeteer = require('puppeteer');

function scrap_images_starting_at_page(pageNum=1){
    puppeteer.launch({ 
        executablePath: '/usr/bin/google-chrome-stable',
        headless: false,
        userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1920,1080'] 
        }).then(async browser => {

            

        function write_to_file(csvCols){
            let string  = "";
                for (var z = 0; z <csvCols.length; z++){
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
        while( !endofentries){ 
            // go to the appropriate base url + if necessary
            try{
                if (pageNum ==1){
                    await page.goto("https://www.zolo.ca/toronto-real-estate/sold");
                } else {
                    await page.goto("https://www.zolo.ca/toronto-real-estate/sold/page-".concat(pageNum.toString(10)));
                }
                if (pageNum == 100){
                    break
                }
            } catch (err){
                throw new PageContactError("page num ".concat(pageNum).concat(" dose not exist"));
            }
            
            // get every link tag
            const urls = await page.$$eval('a', as => as.map(a => a.href));
            // set of used urls so we dont go the same place twice
            let used_urls = new Set();

            for ( var i =0; i<urls.length; i++){
                // use the string in the split function as a delimeter for the url 
                var split =   urls[i].split("https://www.zolo.ca/toronto-real-estate/"); 
                // if the url is a sold house
                if (split[1] != null){
                    var firstChar = split[1][0];
                    // if link is a valid address...
                    if ( !used_urls.has(urls[i]) && firstChar >= '0' && firstChar <='9'){    
                        
                        console.log(urls[i]);
                        console.log(i)
                        used_urls.add(urls[i]);

                        try{
                            await page.goto(urls[i], {waitUntil: 'networkidle2'});  // wait for no more than 2 network connections for 500ms    
                        } catch(err){
                            console.log("SDFSDFSDF")
                            throw new PageContactError("page ".concat(urls[i]).concat(" either doesn't exist or there's a network connection error"));
                        }
                        
                        // check if login pages 
                        try { 
                            await page.$eval('#email', el => el.value = 'svercillo7@gmail.com');
                            await page.click("#formprop1submit")
                        } catch (er) {
                            // pass
                        }

                        try{
                            await page.goto(urls[i], {waitUntil: 'networkidle2'});  // wait for no more than 2 network connections for 500ms    
                        } catch(err){
                            throw new PageContactError("page ".concat(urls[i]).concat(" either doesn't exist or there's a network connection error"));
                        }

                        let pagedata = await page.evaluate(() => {
                            
                        
                            try{
                                // get all the spans
                                let spans =  document.querySelectorAll('span[class="priv"]');
                                
                                // if these conditions are true, page is not a SOLD property 
                                if (spans[5] == undefined || spans[5].innerText.localeCompare("Sold") !=0){
                                    return -3;
                                }

                                // all of these are the same for each page
                                let address =  document.querySelector('section>h1').innerText;
                                let soldOn = spans[6].innerText;
                                
                            } catch(err){
                                return -1
                            }
                        });
                        if (pagedata == -1 || pagedata == -2 || pagedata -3){
                            console.log(pagedata)
                            continue;
                        }

                        let str = pagedata['address'];
                        var j =0;
                        for ( ; j< str.length; j++){
                            if (str[j] == '-'){
                                break;
                            }
                        }
                        if (j != str.length){
                            str = str.substring(j+1);
                        }

                        pagedata['address'] = str;


                        pagedata['pageNum'] = pageNum;
                        pagedata['iterationNum'] = i;
                        pagedata['weblink'] = urls[i]                        

                    }
                }
            }
            pageNum ++;
        }
        
    }).catch(function(error) {
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



scrap_images_starting_at_page()