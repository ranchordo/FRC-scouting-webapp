window = globalThis;
nickname = "null";
var getHTTPResponse = function (url) {
    const request = new XMLHttpRequest();
    request.open('GET', url, false);
    request.send(null);
    if (request.status === 200) {
        return request.responseText;
    } else {
        return "";
    }
}
function pollAssignment() {
    const assignment = getHTTPResponse("/scouter/" + nickname + "/assignment/");
    if (assignment === "none") {
        setTimeout(pollAssignment, 2000);
    } else {
        console.log("Worker: got an assignment " + assignment);
        postMessage(assignment);
    }
}
if (window.Worker) {
    onmessage = function (e) {
        this.nickname = e.data;
        console.log("Worker: got a nickname " + nickname);
        setTimeout(pollAssignment, 100);
    };
}