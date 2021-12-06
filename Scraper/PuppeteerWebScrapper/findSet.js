// find all anomolies in column data on this site

const puppeteer = require('puppeteer');

puppeteer.launch({ 
    executablePath: 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    headless: true,
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1920,1080'] 
    }).then(async browser => {

    const page = await browser.newPage();
    
    var setColumns = new Set();
    var endofentries = false;
    var pageNum = 1
    while( !endofentries){ 
        if (pageNum ==1){
            await page.goto("https://www.zolo.ca/toronto-real-estate/sold");
        } else {
            await page.goto("https://www.zolo.ca/toronto-real-estate/sold/page-".concat(pageNum.toString(10)));
        }

        // get every link tag
        const urls = await page.$$eval('a', as => as.map(a => a.href));
        let used_urls = new Set();
        
        for ( var i =0; i<urls.length; i++){
            var split =   urls[i].split("https://www.zolo.ca/toronto-real-estate/"); 
            if (split[1] != null){
                var firstChar = split[1][0];
                
                // if link is a valid address...
                if ( !used_urls.has(urls[i]) && firstChar >= '0' && firstChar <='9'){    
                    console.log(urls[i]);
                    used_urls.add(urls[i]);
                    await page.goto(urls[i], {waitUntil: 'networkidle2'});
                    
                    // check if login pages 
                    try { 
                        await page.$eval('#email', el => el.value = 'svercillo7@gmail.com');
                        await page.click("#formprop1submit")
                    } catch (er) {
                        // pass
                    }
                    
                    await wait(1000);
                    async function wait(ms) {
                        return new Promise(resolve => {
                            setTimeout(resolve, ms);
                        });
                    }
                    let pagedata = await page.evaluate(() => {
                        let col_names =  document.querySelectorAll('dt[class="column-label"]');
                        let obj = [];                        
                        for (var w =0 ; w < col_names.length; w++){
                            obj.push(col_names[w].innerText);
                        }
                        return obj;
                    });
                
                    pagedata.forEach(ele => {
                        setColumns.add(ele);
                    });
                }
            }
            console.log("SET")
            setColumns.forEach(ele =>{
                console.log( ele)
            })
        }
        pageNum++;
    }
    console.log(setColumns)
    await browser.close();
}).catch(function(error) {
    // console.error(error);
});