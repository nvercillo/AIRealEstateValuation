const puppeteer = require('puppeteer');
 
puppeteer.launch({ 
    // C:\Users\HP USER\Downloads
    // executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true,
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1920,1080'] 
    }).then(async browser => {

    const page = await browser.newPage();
    
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
                    await page.goto(urls[i], {waitUntil: 'networkidle2'});  // wait for no more than 2 network connections for 500ms    
                    
                    // check if login pages 
                    try { 
                        await page.$eval('#email', el => el.value = 'svercillo7@gmail.com');
                        await page.click("#formprop1submit")
                    } catch (er) {
                        // pass
                    }

                    await page.goto(urls[i], {waitUntil: 'networkidle2'});  // this works well
                    
                    // await wait(150000);
                    // async function wait(ms) {
                    //     return new Promise(resolve => {
                    //         setTimeout(resolve, ms);
                    //     });
                    // }

                    let pagedata = await page.evaluate(() => {

                        // create a set of known columns in the middle of the page, check to see nothing weird is coming up
                        const possibleColumns = new Set();
                        possibleColumns.add('Type');
                        possibleColumns.add('Style');
                        possibleColumns.add('Size');
                        possibleColumns.add('Lot Size');
                        possibleColumns.add('Age');
                        possibleColumns.add('Taxes');
                        possibleColumns.add('Walk Score');
                        possibleColumns.add('Days on Site');
                        possibleColumns.add('Pets');
                        possibleColumns.add('Maintenance Fees');
                        possibleColumns.add('Lease Term');
                        possibleColumns.add('Possession');
                        possibleColumns.add('All Inclusive');
                    
                        let spans =  document.querySelectorAll('span[class="priv"]');

                        if (spans[6].innerText.localeCompare("Sold") !=0){
                            return -1;
                        }
                        
                        let col_names =  document.querySelectorAll('dt[class="column-label"]');

                        let temp = [];
                        for (var tt = 0 ; tt < col_names.length; tt++){
                            if (col_names[tt].innerText.localeCompare('Walk Score') != 0){
                                temp.push(col_names[tt]);
                            }
                        }
                        
                        col_names = temp;

                        // constant ? 
                        let address =  document.querySelector('section>h1').innerText;
                        let bedNum = spans[0].innerText;
                        let bathNum = spans[1].innerText;
                        let sqarefootage = spans[2].innerText;
                        let sold_price = spans[3].innerText;
                        let soldOn = spans[5].innerText;

                        
                        // let type = spans[7].innerText;
                        // let style = spans[8].innerText;
                        // let lotSize = spans[10].innerText; // usually null
                        // let age = spans[11].innerText;
                        // let taxes = spans[12].innerText;
                        // let maintenance_fees = spans[13].innerText  

                        obj = 
                        {
                            'sold_price': sold_price,
                            'address' : address,
                            'bedNum': bedNum,
                            'bathNum': bathNum,
                            'sqarefootage' : sqarefootage,
                            'soldOn' : soldOn,
                            'Type' : null,
                            'Style' : null,
                            'Size' : null,
                            'Lot Size' : null,
                            'Age' : null, 
                            'Taxes' : null, 
                            'Walk Score' : null, 
                            'Days on Site': null, 
                            'Pets' : null,
                            'Maintenance Fees' : null,
                            'Lease Term' : null,
                            'Possession' : null,
                            'All Inclusive' : null
                        }
                        
                        var y = 0; 
                        for (var w =0; w < col_names.length; w++){
                            var col = col_names[w+y].innerText;
                            // some weird column name has come up
                            if(!possibleColumns.has(col)){
                                console.log( "ERROR:::::::::::::::::::::::::::")
                                console.log( "ERROR:::::::::::::::::::::::::::")
                                console.log( "ERROR:::::::::::::::::::::::::::")
                                console.log( "ERROR:::::::::::::::::::::::::::")
                                console.log(urls[i]);
                                console.log( "ERROR:::::::::::::::::::::::::::")
                                console.log( "ERROR:::::::::::::::::::::::::::")
                                console.log( "ERROR:::::::::::::::::::::::::::")
                                console.log( "ERROR:::::::::::::::::::::::::::")

                            }
                            // if (col.localeCompare("Walk Score") == 0){
                                obj[col] =  spans[7+ w].innerText;
                            // } else {
                                // obj[col] =  spans[7+ w].innerText;
                            // }
                        }

                        const nearbyCols = [];
                        nearbyCols.push("Groceries");
                        nearbyCols.push("Liquor Store");
                        nearbyCols.push("Restaurants");
                        nearbyCols.push("Coffee");
                        nearbyCols.push("Bank");
                        nearbyCols.push("Gas Station");
                        nearbyCols.push('Health & Fitness');
                        nearbyCols.push("Park");
                        nearbyCols.push("Library");
                        nearbyCols.push("Medical Care");
                        nearbyCols.push("Pharmacy");
                        nearbyCols.push("Mall");
                        nearbyCols.push("Movie Theatre");
                        nearbyCols.push("Bar");


                        let divs =  document.querySelectorAll('div[class="media-heading"]');
                        let dists = document.querySelectorAll('span[class="badge badge--small badge--mono"]')

                        let ndata = {};
                        let arr =[];
                        let lastCol = "";
                        for (var e =0; e<divs.length; e++){
                            let category = false;

                            for (var r = 0; r<nearbyCols.length; r++){
                                let col = nearbyCols[r];
                                if (divs[e].innerText.includes(col)){
                                    category = true;
                                    if (arr.length > 0){
                                        ndata[lastCol] = arr; 
                                        arr = [];
                                    } 
                                    lastCol = col;
                                    break;
                                } 
                            };
                            if (!category ){
                                arr.push(divs[e].innerText);
                            }
                        }

                        delete ndata[""]
                        obj['Amenities'] = ndata;    

                        let schoolRatings = document.querySelectorAll('div[class="media-text"]');
                        let allSchoolType = document.querySelectorAll('div[class="media-sub-heading text-secondary"]');
                        let allSchoolDis = document.querySelectorAll('span[class="badge badge--small badge--mono"]');

                        obj['Nearest Schools'] = []
                        for (var e =0 ;e < schoolRatings.length; e ++){
                            let temp = {};
                            temp['type'] = allSchoolType[allSchoolType.length - schoolRatings.length + e].innerText;
                            temp['distance'] = allSchoolDis[allSchoolDis.length - schoolRatings.length + e].innerText;
                            temp['rating'] = schoolRatings[e].innerText
                            obj['Nearest Schools'].push(temp)
                        }
                        return obj;
                    });
                    if (pagedata == -1){
                        continue;
                    }

                    console.log(pagedata);
                }
            }
        }
    }
    await browser.close();

}).catch(function(error) {
    // console.error(error);
});


