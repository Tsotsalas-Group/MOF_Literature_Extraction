'use strict';
const acs = /acs.org/
const rsc = /rsc.org/
const wiley = /wiley.com/
const sd = /sciencedirect.com/
const ev = /elsevier.com/
const sciences = /sciencemag.org/
const nature = /nature.com/

const puppeteer = require('puppeteer');
const winston = require('winston');
const fs = require('fs');
const path = require('path');


const showUsage = () => {
    console.log('Pbulication Downloading');
    console.log('It is used only for research purposes. You must follow the relevant national laws and regulations during using it.');
    console.log();
    console.log('node manhuagui.js [--filedic ] [--delay ] [--headless] <DOI>');
    console.log();
    console.log('  DOI          :       the DOI of the publication');
    console.log('  --filedic    :       strorage Location. The default value is ".\\"');
    console.log('  --delay      :       delay  before downloading. The default value is 5000 (ms)');
    console.log('  --headless   :       Download using a headless browser (https://en.wikipedia.org/wiki/Headless_browser). The default value is "true"');
};

// Delay
const sleep = (timeout) => new Promise((resolve, reject) => { setTimeout(() => resolve(), timeout); });

// Write file
const w2txtfsM = (txtpath,wordcontent,mode) => {fs.writeFileSync(txtpath, wordcontent, {
    //'w': Open file for writing. The file is created (if it does not exist) or truncated (if it exists).
    //'a': Open file for appending. The file is created if it does not exist.
  flag: mode
});}

// Creat folder
const mkdir = (path) => new Promise((resolve, reject) => {
    fs.mkdir(path, { recursive: true }, (err) => {
        if (err && err.code !== 'EEXIST') {     //  No error when the folder has existed.
            reject(err);
        } else {
            resolve();
        }
    });
});

// Logger 
const logger = winston.createLogger({
    // level: 'debug',
    level: 'http', 
    format: winston.format.combine(

        winston.format.printf(info => `<${info.level}> ${info.message}`)
    ),
    transports: [new winston.transports.Console()]
});

function autoScroll(page,scrollsittings={dirction:1,speed:10}){

    return page.evaluate((scrollsittings) => {

        return new Promise((resolve, reject) => {
            var totalHeight = 0;
            var distance = 100*scrollsittings.dirction;
            var timer = setInterval(() => {
                var scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                if (distance<0){
                    totalHeight += -distance;
                }else{
                    totalHeight += distance;
                }
                if(totalHeight >= scrollHeight){
                    clearInterval(timer);
                    resolve();
                }
            },scrollsittings.speed);
        })
    },scrollsittings);
}

const get_rsc_cont = async (page_f)=>{
    let cont_item = await page_f.$$('article.article-control>div.t-html')
    if ( cont_item.length >0){
        let cont_str = await( await cont_item[0].getProperty('innerHTML')).jsonValue()
        return cont_str
    }
}
const get_rsc_page = async (page_f)=>{
    let cont_item = await page_f.$$('html')
    if ( cont_item.length >0){
        let cont_str = await( await cont_item[0].getProperty('innerHTML')).jsonValue()
        return cont_str
    }
}



const doWork = async (doi_name,options) => {
    let headless_o = (options.headless === 'true')

    // Browser Setting
    const browser = await puppeteer.launch({
        headless: headless_o,
/*      You can also use your own browser
        userDataDir:user_data_path,
        executablePath:chrome_exe, */
    });
    options.userAgent = await browser.userAgent();



    try{
        const page_cont = (await browser.pages())[0];
        await page_cont.setViewport({ width: 1366, height: 768 });
        logger.log('http',`Go to doi page`);
        await page_cont.goto('https://www.doi.org/'+doi_name);

        await sleep(7000)

        await autoScroll(page_cont);

/*         await page_cont.reload() */
        logger.log('http',page_cont.url())
        if (acs.test(page_cont.url())){
            logger.log('debug','acs')
            await acs_cra_cont(page_cont,options)
        }else if(rsc.test(page_cont.url())){
            logger.log('debug','rsc')
            await rsc_cra_cont(page_cont,options)
        }else if(wiley.test(page_cont.url())){
            logger.log('debug','wiley')
            await wiley_cra_cont(page_cont,options)
        }else if(sd.test(page_cont.url())){
            logger.log('debug','sd')
            await sd_cra_cont(page_cont,options)
        }else if(ev.test(page_cont.url())){
            logger.log('debug','sd')
            await sd_cra_cont(page_cont,options)
        }else if(sciences.test(page_cont.url())){
            logger.log('debug','sciences')
            await sciences_cra_cont(page_cont,options)
        }
        else{
            throw 'not_included'
        }
    }catch(err){
        logger.error(err)
        await browser.close()
    }
    await browser.close();
}

const rsc_cra_cont = async (page_cont,options) =>{

    let acs_url = page_cont.url();

    //make sure the url is full and right
    if (/\/articlelanding\//.test(acs_url) === false){
        if (/doi\/abs/.test(acs_url) === true){
            acs_url = acs_url.replace('/articlehtml/','/articlelanding/')
        }
        await page_cont.goto(acs_url,{waitUntil: 'load',timeout: 90000});
    }

    /*     //copyright check!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        let cori_item = await page_cont.$$('h4.access-denied-msg')
        if ( cori_item.length >0){
            logger.log('warn','copyright_missing')
            // down_acs_si(page_cont,option)
        }
    */

    //get main text
    let cont_str = '';
    let cont_try = 0;
    let move_dirc = 1;
    while(cont_str === '' && cont_try<10){
        await autoScroll(page_cont,{dirction:move_dirc,spped:100,});
        cont_str = await get_rsc_cont(page_cont);
        move_dirc = -move_dirc;
        cont_try ++;
    }

    if (cont_str === ''){
        logger.log('warn','unknow_content_error')
    }else{
        w2txtfsM(path.join(options.filedic,'main_text.html'),cont_str,'w')

    }

    //get Si
    let si_item = await page_cont.$$('ul.list__collection>li.list__item--dashed>a')
    let si_number = si_item.length;

    if ( si_number >0){
        let totla_si =0;
        for (let si_order = 0; si_order < si_number ;si_order++){
            let si_str = await (await si_item[si_order].getProperty('href')).jsonValue();
            if (typeof si_str === 'string'){
                logger.log('info',si_str);
                totla_si++;
            }
        }
        logger.log('info',`${totla_si}`);
        logger.log('info','SI_ava');

    }

    acs_url = acs_url.replace('/articlelanding/','/articlehtml/');
    await page_cont.goto(acs_url,{waitUntil: 'load',timeout: 90000});
    logger.log('http','redirect to html_page');
    let cont_page = await get_rsc_page(page_cont);
    w2txtfsM(path.join(options.filedic,'full_page.html'),'<html>\n'+cont_page+'\n</html>','w')
    logger.info('full_page is downloaded.')
}

const acs_cra_cont = async (page_cont,options) =>{

    let acs_url = page_cont.url();

    if (/\/full\//.test(acs_url) === false){
        if (/doi\/abs/.test(acs_url) === true){
            acs_url = acs_url.replace('/doi/abs/','/doi/full/')
        }else{
            acs_url = acs_url.replace('/doi/','/doi/full/')
        }
        await page_cont.goto(acs_url,{waitUntil: 'load',timeout: 90000});
    }

    let cori_item = await page_cont.$$('h4.access-denied-msg');
    if ( cori_item.length >0){
        logger.log('warn','copyright_missing')
        // down_acs_si(page_cont,option)
    }

    let cont_item = await page_cont.$$('div.article_content-left.hlFld-FullText.ui-resizable');
    if ( cont_item.length >0){
        let cont_str = await (await cont_item[0].getProperty('innerHTML')).jsonValue();
        w2txtfsM(path.join(options.filedic,'main_text.html'),cont_str,'w');
        logger.info('Main context is downloaded.')
    }
    let si_item = await page_cont.$$('.sup-info-attachments>ul>li.decorationNone>ul>li>a.suppl-anchor');
    let si_number = Math.floor(si_item.length/2);

    if ( si_number >0){
        let totla_si =0;
        for (let si_order = 0; si_order < si_number ;si_order++){
            let si_str = await (await si_item[si_order].getProperty('href')).jsonValue();
            if (typeof si_str === 'string'){
                logger.log('info',si_str);
                totla_si++;
            }
        }
        logger.log('info',`${totla_si}`);
        logger.log('info','SI_ava');

    }
    let cont_page_item = await page_cont.$$('html');
    let cont_page = await (await cont_page_item[0].getProperty('innerHTML')).jsonValue();
    w2txtfsM(path.join(options.filedic,'full_page.html'),'<html>\n'+cont_page+'\n</html>','w')
    logger.info('full_page is downloaded.')
}


const wiley_cra_cont = async (page_cont,options) =>{

    let wiley_url = page_cont.url();

    if (/\/full\//.test(wiley_url) === false){
        if (/doi\/abs/.test(wiley_url) === true){
            wiley_url = wiley_url.replace('/doi/abs/','/doi/full/')
        }else{
            wiley_url = wiley_url.replace('/doi/','/doi/full/')
        }
        await page_cont.goto(wiley_url,{waitUntil: 'load',timeout: 90000});
    }


    //Deutesch Website....
    if (/\/ange\./.test(wiley_url) === true){

        wiley_url = wiley_url.replace('/\/ange\./','/\/anie\./');
        await page_cont.goto(wiley_url,{waitUntil: 'load',timeout: 90000});
    }

    let cori_item = await page_cont.$$('h4.access-denied-msg');
    if ( cori_item.length >0){
        throw 'copyright_missing'
        // down_acs_si(page_cont,option)
    }

    let cont_item = await page_cont.$$('div[class="row article-row"] div#article__content');
    if ( cont_item.length >0){
        let cont_str = await (await cont_item[0].getProperty('innerHTML')).jsonValue();
        w2txtfsM(path.join(options.filedic,'main_text.html'),cont_str,'w');
        logger.info('Main context is downloaded.')
    }


    let si_item = await page_cont.$$('table[class="support-info__table table article-section__table"]>tbody tr a')
    let si_number = si_item.length;

    if ( si_number >0){
        let totla_si =0
        for (let si_order = 0; si_order < si_number ;si_order++){
            let si_str = await (await si_item[si_order].getProperty('href')).jsonValue();
            if (typeof si_str === 'string'){
                logger.log('info',si_str);
                totla_si++;
            }
        }
        logger.log('info',`${totla_si}`);
        logger.log('info','SI_ava');

    }

    let cont_page_item = await page_cont.$$('html')
    let cont_page = await (await cont_page_item[0].getProperty('innerHTML')).jsonValue();
    w2txtfsM(path.join(options.filedic,'full_page.html'),'<html>\n'+cont_page+'\n</html>','w')
    logger.info('full_page is downloaded.')

}

const sd_cra_cont = async (page_cont,options) =>{

    let sc_url = page_cont.url()

    //make sure the url is full and right
    if (/article\/abs/.test(sc_url) === true){
        sc_url = sc_url.replace('/article\/abs/','/article/');
        await page_cont.goto(acs_url,{waitUntil: 'load',timeout: 90000});
    }

    //copyright check!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    let cori_item = await page_cont.$$('div[class="buttons text-s"] div[class="PdfDownloadButton u-display-inline-block"] span[class="button-text"] span')

    if ( cori_item.length >0){
        let check_str = await(await cori_item[0].getProperty('textContent')).jsonValue()
        if (check_str === "Get Access"){
            throw 'copyright_missing'
        }
    }


    //get main text
    await autoScroll(page_cont);

    let cont_item = await page_cont.$$('article[class="col-lg-12 col-md-16 pad-left pad-right"]')
    if ( cont_item.length >0){
        let cont_str = await (await cont_item[0].getProperty('innerHTML')).jsonValue()
        w2txtfsM(path.join(options.filedic,'main_text.html'),cont_str,'w')
        logger.info('Main context is downloaded.')
    }


    //get Si
    let si_item = await page_cont.$$('div[class="Appendices"] a[class="icon-link"]')
    let si_number = si_item.length;

    if ( si_number >0){
        let totla_si =0
        for (let si_order = 0; si_order < si_number ;si_order++){
            let si_str = await (await si_item[si_order].getProperty('href')).jsonValue()
            if (typeof si_str === 'string'){
                logger.log('info',si_str);
                totla_si++;
            }
        }
        logger.log('info',`${totla_si}`);
        logger.log('info','SI_ava');

    }

    let cont_page_item = await page_cont.$$('html');
    let cont_page = await (await cont_page_item[0].getProperty('innerHTML')).jsonValue();
    w2txtfsM(path.join(options.filedic,'full_page.html'),'<html>\n'+cont_page+'\n</html>','w')
    logger.info('full_page is downloaded.')

}

const sciences_cra_cont = async (page_cont,options) =>{

    let sc_url = page_cont.url();

    let azbs_check = await page_cont.$$('div[class="highwire-markup"] a[class="hw-link hw-link-article-full-text"]')
    if ( azbs_check.length >0){
       let full_lin_str =  await(await cori_item[0].getProperty('href')).jsonValue()
       await page_cont.goto(full_lin_str,{waitUntil: 'load',timeout: 90000});
    }

    //copyright check!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    let cori_item = await page_cont.$$('div[class="panel-pane pane-sci-purchase-links"] li[class="purchase first last"]')

    if ( cori_item.length >0){

        throw 'copyright_missing'

    }


    //get main text
    await autoScroll(page_cont);

    let cont_item = await page_cont.$$('div[class="pane-content"] div[class="article fulltext-view"]')
    if ( cont_item.length >0){
        let cont_str = await (await cont_item[0].getProperty('innerHTML')).jsonValue()
        w2txtfsM(path.join(options.filedic,'main_text.html'),cont_str,'w')
        logger.info('Main context is downloaded.')
    }


    let cont_page_item = await page_cont.$$('html')
    let cont_page = await (await cont_page_item[0].getProperty('innerHTML')).jsonValue()
    w2txtfsM(path.join(options.filedic,'full_page.html'),'<html>\n'+cont_page+'\n</html>','w')
    logger.info('full_page is downloaded.')
}


const argv = require('minimist')(process.argv.slice(2));
if (!argv._ || argv._.length === 0 || argv.help || argv.version) {
    showUsage();
} else {

    doWork(argv._, {
        filedic: argv.filedic || ".\\",
        delay: argv.delay || 5000,
        headless: argv.headless || 'true'
    });}



// doWork('10.1016/j.inoche.2012.10.038',{
//     filedic:".\\",
//     delay:5000,
//     headless:'flase'
// })
