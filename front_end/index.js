// Counter


const decreaseBtn = document.getElementById("decrease");
const resetBtn = document.getElementById("reset");
const increaseBtn = document.getElementById("increase");
const counter = document.getElementById("counter");
let count = 0;

increaseBtn.onclick = function() {
    count++;
    counter.textContent = count;
}

decreaseBtn.onclick = function() {
    count--;
    counter.textContent = count;
}

resetBtn.onclick = function() {
    count = 0;
    counter.textContent = count;
}
