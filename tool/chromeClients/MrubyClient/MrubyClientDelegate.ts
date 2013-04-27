/**
	mruby Client
*/

var currentFilterName = "mruby";

// settings for mruby
var mrbcPath = "/Users/sassembla/test/mruby/bin/mrbc";
var mrubyPath = "/Users/sassembla/test/mruby/bin/mruby";


var MODE_MRBC = 0;
var MODE_MRUBY = 1;

// runshell path (if you want to switch mrbc/mruby, change below.)
var MRB_RUN_MODE = MODE_MRBC;


// SublimeSocket setting
var CURRENT_SETTING_PATH = "SUBLIMESOCKET_PATH:tool/chromeClients/MrubyClient/mrubyFilter.txt";


var MRB_CONVERT_SHELLPATH = "SUBLIMESOCKET_PATH:tool/chromeClients/MrubyClient/mrubyconv.sh";
var MRB_MRUBY_SHELLPATH = "SUBLIMESOCKET_PATH:tool/chromeClients/MrubyClient/mruby.sh";


var TSC_TYPESCRIPTFILE_WILDCARD = "*.rb";


var TARGET_FOCUSED = 0;
var TARGET_FOLDER = 1;

var TSC_COMPILATIONTARGETMODE = TARGET_FOLDER;


// tsc specific trigger.
var TSC_CHECKVERSIONRESULT = "API VERIFIED:"
var TSC_IDENTIFIED_SENDER_STARTMARK = "mrubysaved";
var TSC_IDENTIFIED_SENDER_ENDMARK = "mrubyfinished";


class MrubyClientDelegate extends ExtensionDelegate {
	
	constructor (tab) {
		super(tab);
	}

  onOpen (delegate:ExtensionDelegate, e) {
  	delegate.send("ss@runSetting:"+JSON.stringify({"path":CURRENT_SETTING_PATH}));
  }

  onMessage (delegate:ExtensionDelegate, e) {
  	if (e.data.indexOf(TSC_CHECKVERSIONRESULT) === 0) {
  		console.log("checkVersion result:   "+e.data);
  		return;
  	}

  	if (e.data.indexOf(TSC_IDENTIFIED_SENDER_STARTMARK) === 0) {
		  //ここですでにコンパイル中かどうかのチェックが可能ではある。状態持つとしたらここ。
		  if (!delegate.isLocked()) {
		  	delegate.unlock();
	  	} else {
	  		return;
	  	}

	  	console.log("compile start");

		  var currentCompileTargetFileName = e.data.replace(TSC_IDENTIFIED_SENDER_STARTMARK+":","")
		  if (currentCompileTargetFileName.indexOf(this.currentTargetFolderPath) !== -1) {
				// exist in target folder.
			} else {
				return;
			}


			var runTargetShell;
			var runTargetCommandPath;
			switch (MRB_RUN_MODE) {
				case MODE_MRBC:
				runTargetShell = MRB_CONVERT_SHELLPATH;
				runTargetCommandPath = mrbcPath;
				break;

				case MODE_MRUBY:
				runTargetShell = MRB_MRUBY_SHELLPATH;
				runTargetCommandPath = mrubyPath;
				break;
			}

			var runShellJSON;
			switch (TSC_COMPILATIONTARGETMODE) {
				case TARGET_FOCUSED:
				runShellJSON = {
					"main": "/bin/sh",
					"":[
					runTargetShell,
					runTargetCommandPath,
					currentCompileTargetFileName,
					this.currentTargetFolderPath + this.currentCompilationLogFileName
					],
					"debug":true
				};
				break;

				case TARGET_FOLDER:
				runShellJSON = {
					"main": "/bin/sh",
					"": [
					runTargetShell,
					runTargetCommandPath,
					this.currentTargetFolderPath + TSC_TYPESCRIPTFILE_WILDCARD,
					this.currentTargetFolderPath + this.currentCompilationLogFileName
					],
					"debug":true
				};
				break;
			}

			var command = "ss@runShell:"+JSON.stringify(runShellJSON);

			delegate.send(command);
			
			return;
		}

		if (e.data.indexOf(TSC_IDENTIFIED_SENDER_ENDMARK) === 0) {
			console.log("compiled");
			delegate.lock();
			return;
		}
	}

	tailed (delegate:ExtensionDelegate, text:string) {
		console.log("result:"+text);
		var lines = text.split("\n");
		for (var i = 0; i < lines.length; i++) {
			var line = lines[i].replace(/"/g,"_");


			var filteringJSON = {
				"name":currentFilterName,
				"source":line
			};
			if (lines[i] != '') {
				delegate.send("ss@filtering:"+JSON.stringify(filteringJSON));
			}
		}
	}

}