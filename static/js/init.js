// record start & set time in sessionStorage
function record_start() {
    const startTimeOfRecord = Date.now();
    sessionStorage.setItem("startTimeOfRecord", startTimeOfRecord);
}

// show recording time when on-air per 1 minutes
setInterval(function () {
    const Time = document.getElementById("presentTime");
    const recordingTime = new Date();
    Time.innerText = recordingTime.toLocaleString();

    const Target = document.getElementById("recordingClock");
    const startTimeOfRecord = parseInt(sessionStorage.getItem("startTimeOfRecord"));

    if (Target){

        const hours = parseInt((recordingTime - startTimeOfRecord) / 1000 / 60 / 60);
        const minutes = parseInt((recordingTime - startTimeOfRecord) / 1000 / 60);
        const seconds = parseInt((recordingTime - startTimeOfRecord) / 1000);
        
        Target.innerText = `${hours > 10 ? `0${hours}` : hours}:${minutes < 10 ? `0${minutes}` : minutes}:${
            seconds < 10 ? `0${seconds}` : seconds
        }`;
    }
}, 1000 * 0.5);
