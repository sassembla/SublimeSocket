/**
	Scala Client
*/

var currentFilterName = "scala";

// settings for TypeScript
var CURRENT_SETTING_PATH = "SUBLIMESOCKET_PATH:tool/chromeClients/ScalaClient/ScalaFilter.txt";

/**
	Scalaの場合は、Gradleを使って簡単なプロジェクトをビルドするところからやってみればいいと思う。
	sbt、、は、、うーん、、
	まずGradleで動くようにする。次に、

	gradle test
*/
var SCALA_GRADLE_SHELLPATH = "SUBLIMESOCKET_PATH:tool/chromeClients/ScalaClient/scalaShell.sh";

// tsc specific trigger.
var TSC_CHECKVERSIONRESULT = "API VERIFIED:"

// tail開始のサインなので、必要。
var SCALAC_IDENTIFIED_SENDER_STARTMARK = "scalasaved";
var SCALAC_IDENTIFIED_SENDER_ENDMARK = "scalacompilefinished";


class ScalaClientDelegate extends ExtensionDelegate {
	
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

  	if (e.data.indexOf(SCALAC_IDENTIFIED_SENDER_STARTMARK) === 0) {
  		if (!delegate.isLocked()) {
		  	delegate.unlock();
	  	} else {
	  		return;
	  	}

	  	console.log("compile start");

		  var currentCompileTargetFileName = e.data.replace(SCALAC_IDENTIFIED_SENDER_STARTMARK+":","")
		  if (currentCompileTargetFileName.indexOf(this.currentTargetFolderPath) !== -1) {
				// exist in target folder.
			} else {
				return;
			}

			console.log("SCALA_GRADLE_SHELLPATH"+SCALA_GRADLE_SHELLPATH);
			var runShellJSON = {
				"main": "/bin/sh",
				"":[
					SCALA_GRADLE_SHELLPATH,
					this.currentTargetFolderPath,
					this.currentTargetFolderPath + this.currentCompilationLogFileName
				]
			};

			var command = "ss@runShell:"+JSON.stringify(runShellJSON);

			delegate.send(command);
			
			return;
		}

		if (e.data.indexOf(SCALAC_IDENTIFIED_SENDER_ENDMARK) === 0) {
			console.log("compiled");
			delegate.lock();
			return;
		}
	}

	tailed (delegate:ExtensionDelegate, text:string) {
		console.log("result:"+text);
		var lines = text.split("\n");
		for (var i = 0; i < lines.length; i++) {
			var filteringJSON = {
				"name":currentFilterName,
				"source":lines[i]
			};
			if (lines[i] != '') {
				delegate.send("ss@filtering:"+JSON.stringify(filteringJSON));
			}
		}
	}

}