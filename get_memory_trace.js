const fs = require('fs');
const Chrome = require('chrome-remote-interface');

let TRACE_CATEGORIES = ["-*","memory", "disabled-by-default-memory-infra", "disabled-by-default-memory-infra.v8.code_stats"]
let rawEvents = [];

website_to_load = process.argv[3]
website_name = process.argv[2]

Chrome(async function (chrome) {
    with (chrome) {
		Page.enable();
		
		await Network.clearBrowserCache();
        await Network.clearBrowserCookies();
        console.log('Cleared cache and cookies!')
		
		Tracing.start({
            "categories":   TRACE_CATEGORIES.join(','),
            "options":      "sampling-frequency=10000"  // 1000 is default and too slow.
        });
        console.log("Loading :" + website_name)

        Page.navigate({'url': website_to_load})
        Page.loadEventFired(async function () {
			guid = await Tracing.requestMemoryDump()
			Tracing.end()
        });

        Tracing.tracingComplete(function () {
            let file = './traces/'+ website_name + '-' + Date.now() + '.devtools.trace';
            fs.writeFileSync(file, JSON.stringify(rawEvents, null, 2));
            console.log('Trace file stored at: ' + file);
            console.log("Done!")
            chrome.close();
        });

        Tracing.dataCollected(function(data){
            let events = data.value;
            rawEvents = rawEvents.concat(events);
        });
	}
	
}).on('error', function (e) {
    console.error('Cannot connect to Chrome', e);
});
