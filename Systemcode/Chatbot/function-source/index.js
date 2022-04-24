// See https://github.com/dialogflow/dialogflow-fulfillment-nodejs
// for Dialogflow fulfillment library docs, samples, and to report issues
'use strict';

// try without jshint and with
/* jshint esversion: 8 */

const functions = require('firebase-functions');
const {WebhookClient} = require('dialogflow-fulfillment');
const {Card, Suggestion} = require('dialogflow-fulfillment');
const axios = require('axios');
 
process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements
 
exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });
  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));
  
    let unit_weight;
    let unit_length;
    let unit_width;
    let unit_height;

    let final_weight;
    let final_length;
    let final_width;
    let final_height;
    let query = {
        "username":"lyra.li@cxrus.com",
        "api_key":"5f7f41cef2b379133c496efbd95499b3",
        "items":
        [
            {
                "id":"items",
                "w":0,
                "h":0,
                "d":0,
                "wg":0,
                "q":0,
                "vr":true
            }
        ],
        "bins":
        [
            {
                "id":"Max Box Size",
                "h":200,
                "w":200,
                "d":200,
                "wg":"",
                "max_wg":""
            }
        ],
        "params":
        {
            "images_background_color":"255,255,255",
            "images_bin_border_color":"59,59,59",
            "images_bin_fill_color":"230,230,230",
            "images_item_border_color":"22,22,22",
            "images_item_fill_color":"255,193,6",
            "images_item_back_border_color":"22,22,22",
            "images_sbs_last_item_fill_color":"177,14,14",
            "images_sbs_last_item_border_color":"22,22,22",
            "images_format":"svg",
            "images_width":50,
            "images_height":50,
            "images_source":"file",
            "stats":0,
            "item_coordinates":1,
            "images_complete":1,
            "images_sbs":1,
            "images_separated":0
        }
    };   
//   function packaging(agent) {
//     const item = agent.parameters.item;
//     const quantity = agent.parameters.quantity;
//     getData();
//     //agent.add(`Weight: ${final_weight} kg`);
//   }
async function getData(agent) {
    const item = agent.parameters.item;
    const quantity = agent.parameters.quantity;
    let result  = await apiCall(`https://sheetdb.io/api/v1/6v137hb0uccis/search?name=*${item}*`);
    console.log('sssss', result);

    if (result) {
        query.items[0].wg = result[0].weight;
        query.items[0].d = result[0].length;
        query.items[0].w = result[0].width;
        query.items[0].h = result[0].height;
        query.items[0].q = quantity;
    
    }
    console.log('sdsfdfsfsd',query.items[0].w);
    let result1 = await apiCall('https://asia1.api.3dbinpacking.com/packer/findBinSize',{ params: { query: JSON.stringify(query) } });
    if (result1) {
        final_weight = result1.response.bins_packed[0].bin_data.weight;
        final_length = result1.response.bins_packed[0].bin_data.d;
        final_width = result1.response.bins_packed[0].bin_data.w;
        final_height = result1.response.bins_packed[0].bin_data.h;
    
    }
    console.log('newnew', result1.response.bins_packed[0].bin_data.weight, final_weight);
    agent.add(`For your shipment, please fill in the form with the following info: Weight: ${final_weight} kg, Length: ${final_length} cm, Width: ${final_width} cm, Height: ${final_height} cm`)
   }
    
function apiCall(url, query) {
        return new Promise((resolve, reject) => {
        axios.get(url, query).then(function(res) {
            console.log('WWWWWWWWWWWWW', res);
            resolve(res.data);
            });
        });
    }
  // Run the proper function handler based on the matched Dialogflow intent name
  let intentMap = new Map();
  intentMap.set('PhoneIntent', getData);
  intentMap.set('PackageIntent', getData);
  intentMap.set('Electric.TV.56-inchIntent', getData);
  intentMap.set('Electronics.PhoneIntent', getData);
  intentMap.set('Documents.LettersIntent', getData);
  intentMap.set('Documents.TicketsIntent', getData);
  intentMap.set('Documents.PassportsIntent', getData);
  intentMap.set('Documents.Gift and Reward CardsIntent', getData);
  intentMap.set('Documents.Greeting cards Intent', getData);

  intentMap.set('Documents.Lecture notesIntent', getData);
  intentMap.set('Documents.Journals  and MagazinesIntent', getData);
  intentMap.set('Documents.BooksIntent', getData);
  intentMap.set('Documents.Legal notices and billsIntent', getData);
  intentMap.set('Documents.Cheque bookIntent', getData);


  intentMap.set('Clothing.T-shirtsIntent', getData);
  intentMap.set('Clothing.DressIntent', getData);
  intentMap.set('Clothing.Winter Wear Intent', getData);

  intentMap.set('Clothing.Swim WearIntent', getData);
  intentMap.set('Clothing.Athlete ClothesIntent', getData);
  intentMap.set('Clothing.Coats and JacketsIntent', getData);

  intentMap.set('Clothing.CostumesIntent', getData);
  intentMap.set('Clothing.Baby wearIntent', getData);
  intentMap.set('Clothing.Scarves and TiesIntent', getData);
  intentMap.set('Clothing.Cap and hatsIntent', getData);


  intentMap.set('Electronics.PhonesIntent', getData);
  intentMap.set('Electronics.CameraIntent', getData);
  intentMap.set('Electronics.TVIntent', getData);


  intentMap.set('Electronics.iPadIntent', getData);


  intentMap.set('Electronics.Chargers, Plugs and remoteIntent', getData);
  intentMap.set('Electronics.LaptopIntent', getData);
  intentMap.set('Electronics.Iron boxIntent', getData);
  intentMap.set('Electronics.Table top AppliancesIntent', getData);

  intentMap.set('Electronics.Vacuum CleanerIntent', getData);
  intentMap.set('Electronics.Video game ConsoleIntent', getData);
  intentMap.set('Electronics.Lamps and bulbsIntent', getData);


  intentMap.set('Lifestyle.Wrist WatchesIntent', getData);
  intentMap.set('Lifestyle.BeltsIntent', getData);
  intentMap.set('Lifestyle.Jewellery and AccessoriesIntent', getData);

  intentMap.set('Lifestyle.BootsIntent', getData);
  intentMap.set('Lifestyle.Sneakers amd shoesIntent', getData);
  intentMap.set('Lifestyle.Perfumes and spraysIntent', getData);
  intentMap.set('Lifestyle.HandbagsIntent', getData);
  intentMap.set('Lifestyle.BackpacksIntent', getData);
  intentMap.set('Lifestyle.Purses and WalletsIntent', getData);
  intentMap.set('Lifestyle.Sunglasses and SpectaclesIntent', getData);



  intentMap.set('HomeNeeds.CurtainsIntent', getData);
  intentMap.set('HomeNeeds.CushionsIntent', getData);
  intentMap.set('HomeNeeds.BedlinenIntent', getData);
  intentMap.set('HomeNeeds.RugsIntent', getData);


  intentMap.set('HomeNeeds.BlanketsIntent', getData);

  intentMap.set('HomeNeeds.Artwork and Wall mountsIntent', getData);
  intentMap.set('HomeNeeds.Picture framesIntent', getData);
  intentMap.set('HomeNeeds.SculpturesIntent', getData);

  intentMap.set('HomeNeeds.PillowsIntent', getData);
  intentMap.set('HomeNeeds.Office suppliesIntent', getData);



  intentMap.set('PersonalCare.Shampoo and ConditionerIntent', getData);

  intentMap.set('PersonalCare.Tooth PasteIntent', getData);
  intentMap.set('PersonalCare.Cleaning LiquidsIntent', getData);

  intentMap.set('PersonalCare.Cosmetic ItemsIntent', getData);
  intentMap.set('PersonalCare.BrushesIntent', getData);

  intentMap.set('PersonalCare.Shaving razorsIntent', getData);
  intentMap.set('PersonalCare.Creams and lotionsIntent', getData);
  intentMap.set('PersonalCare.Sponges and scrub padsIntent', getData);
  intentMap.set('PersonalCare.DiapersIntent', getData);

  intentMap.set('PersonalCare.Tissue boxIntent', getData);


  intentMap.set('KitchenEssentials.ContainersIntent', getData);

  intentMap.set('KitchenEssentials.Cutting boardIntent', getData);
  intentMap.set('KitchenEssentials.Cooking utensilsIntent', getData);

  intentMap.set('KitchenEssentials.ChopperIntent', getData);
  intentMap.set('KitchenEssentials.OpenersIntent', getData);
  intentMap.set('KitchenEssentials.CrockeryIntent', getData);

  intentMap.set('KitchenEssentials.CutleryIntent', getData);
  intentMap.set('KitchenEssentials.Mixing bowlIntent', getData);
  intentMap.set('KitchenEssentials.Baking AccessoriesIntent', getData);


  intentMap.set('KitchenEssentials.Serving Spoons and ladlesIntent', getData);

  intentMap.set('Food.VegetablesIntent', getData);

  intentMap.set('Food.FruitsIntent', getData);

  intentMap.set('Food.Canned FoodsIntent', getData);
  intentMap.set('Food.HampersIntent', getData);

  intentMap.set('Food.GroceriesIntent', getData);

  intentMap.set('Food.DrinksIntent', getData);

  intentMap.set('Food.Grains and CerealsIntent', getData);

  intentMap.set('Food.Condiments and spicesIntent', getData);
  intentMap.set('Food.Rice and pastaIntent', getData);

  intentMap.set('Food.Cooking oilIntent', getData);



  intentMap.set('Health.Medicines and SupplementsIntent', getData);

  intentMap.set('Health.First Aid kitsIntent', getData);
  intentMap.set('Health.Weighing scaleIntent', getData);
  intentMap.set('Health.Sanitising and cleaning liquids Intent', getData);

  intentMap.set('Health.BP and heart rate monitorsIntent', getData);
  intentMap.set('Health.Mask boxesIntent', getData);
  intentMap.set('Health.Yoga and tumbling matsIntent', getData);
  intentMap.set('Health.Walking stickIntent', getData);
  intentMap.set('Health.Skipping ropes and resistance bandsIntent', getData);
  intentMap.set('Health.TonicIntent', getData);


  intentMap.set('Entertainment .Cuddly toysIntent', getData);
  intentMap.set('Entertainment .Board gamesIntent', getData);
  intentMap.set('Entertainment .PuzzlesIntent', getData);
  intentMap.set('Entertainment .ToysIntent', getData);
  intentMap.set('Entertainment .Outdoor gamesIntent', getData);
  intentMap.set('Entertainment .Sports EquipmentIntent', getData);

  intentMap.set('Entertainment .Gardening suppliesIntent', getData);
  intentMap.set('Entertainment .Craft itemsIntent', getData);

  intentMap.set('Entertainment .CDs and DVDsIntent', getData);
  intentMap.set('Entertainment .SouvenirsIntent', getData);
  intentMap.set('Entertainment .TrophyIntent', getData);

  // 3rd level intents

  intentMap.set('Documents.greeting_cards_small', getData);
  intentMap.set('Documents.greeting_cards_large', getData);




  intentMap.set('Clothing.winter_wear_light', getData);
  intentMap.set('Clothing.winter_wear_heavy', getData);


  intentMap.set('Clothing.coats_and_jackets_light', getData);
  intentMap.set('Clothing.coats_and_jackets_heavy', getData);






  intentMap.set('Electronics.tv-32', getData);
  intentMap.set('Electronics.tv-60', getData);
  intentMap.set('Electronics.tv-80', getData);
  intentMap.set('Electronics.ipad_air', getData);
  intentMap.set('Electronics.ipad_pro', getData);
  intentMap.set('Electronics.ipad_mini', getData);



  intentMap.set('Electronics.table_top_appliances_small', getData);
  intentMap.set('Electronics.table_top_appliances_large', getData);







  intentMap.set('Lifestyle.jewellery_and_accessories_light', getData);
  intentMap.set('Lifestyle.jewellery_and_accessories_heavy', getData);





  intentMap.set('HomeNeeds.rugs_light', getData);
  intentMap.set('HomeNeeds.rugs_medium', getData);
  intentMap.set('HomeNeeds.rugs_heavy', getData);
  intentMap.set('HomeNeeds.blankets_light', getData);
  intentMap.set('HomeNeeds.blankets_heavy', getData);


  intentMap.set('HomeNeeds.sculptures_light', getData);
  intentMap.set('HomeNeeds.sculptures_heavy', getData);

  intentMap.set('HomeNeeds.office_supplies', getData);



  intentMap.set('PersonalCare.shampoo_conditioner_samll_16', getData);
  intentMap.set('PersonalCare.shampoo_conditioner_big_34', getData);

  intentMap.set('PersonalCare.cleaning_liquids_small_16', getData);
  intentMap.set('PersonalCare.cleaning_liquids_small_34', getData);

  intentMap.set('PersonalCare.brushes_clearning', getData);
  intentMap.set('PersonalCare.brushes_make_up', getData);



  intentMap.set('PersonalCare.diapers_small', getData);
  intentMap.set('PersonalCare.diapers_big', getData);



  intentMap.set('KitchenEssentials.containers_small', getData);
  intentMap.set('KitchenEssentials.containers_big', getData);

  intentMap.set('KitchenEssentials.cooking_utensils_small', getData);
  intentMap.set('KitchenEssentials.cooking_utensils_big', getData);


  intentMap.set('KitchenEssentials.crockery_small', getData);
  intentMap.set('KitchenEssentials.crockery_big', getData);


  intentMap.set('KitchenEssentials.baking_accessories_small', getData);
  intentMap.set('KitchenEssentials.baking_accessories_medium', getData);
  intentMap.set('KitchenEssentials.baking_accessories_big', getData);


  intentMap.set('Food.vegetables_small', getData);
  intentMap.set('Food.vegetables_big', getData);
  intentMap.set('Food.fruits_small', getData);
  intentMap.set('Food.fruits_big', getData);

  intentMap.set('Food.hampers_small', getData);
  intentMap.set('Food.hampers_big', getData);
  intentMap.set('Food.groceries_small', getData);
  intentMap.set('Food.groceries_big', getData);
  intentMap.set('Food.drinks_small', getData);
  intentMap.set('Food.drinks_big', getData);
  intentMap.set('Food.grains_and_cereals_small', getData);
  intentMap.set('Food.grains_and_cereals_big', getData);

  intentMap.set('Food.rice_and_pasta_small', getData);
  intentMap.set('Food.rice_and_pasta_big', getData);
  intentMap.set('Food.cooking_oil_small', getData);
  intentMap.set('Food.cooking_oil_big', getData);


  intentMap.set('Health.medicines_and_supplements_small', getData);
  intentMap.set('Health.medicines_and_supplements_big', getData);


  intentMap.set('Health.sanitising_and_cleaning_liquids_small', getData);
  intentMap.set('Health.sanitising_and_cleaning_liquids_big', getData);



  intentMap.set('Entertainment .sports_equipment_small', getData);
  intentMap.set('Entertainment .sports_equipment_big', getData);

  intentMap.set('Entertainment .craft_items_small', getData);
  intentMap.set('Entertainment .craft_items_big', getData);
  
  agent.handleRequest(intentMap);
});