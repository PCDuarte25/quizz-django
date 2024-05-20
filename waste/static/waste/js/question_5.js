const EMPTY_BIN_CLASS = 'empty-bin';
const THROWN_ITEM_CLASS = 'thrown-item';

const BATTERY_ID = 'battery'
const APPLE_ID = 'apple'
const SODA_ID = 'soda'

const battery = document.getElementById(BATTERY_ID);
const apple = document.getElementById(APPLE_ID);
const soda = document.getElementById(SODA_ID);

const batteryBin = document.getElementById('battery-bin');
const metalBin = document.getElementById('metal-bin');
const organicBin = document.getElementById('organic-bin');

const batteryBinInput = document.getElementById('battery-bin-input');
const metalBinInput = document.getElementById('metal-bin-input');
const organicBinInput = document.getElementById('organic-bin-input');

const form = document.getElementById('form');

const items = [
  battery,
  apple,
  soda,
];

const bins = [
  batteryBin,
  metalBin,
  organicBin,
];

let draggedItem = null;

form.addEventListener('submit', (e) => {
  // for (const bin of bins) {
  //   if (isBinEmpty(bin)) {
  //     e.preventDefault()
  //     alert('safado');
  //     return;
  //   }
  // }

  batteryBinInput.value = batteryBin.dataset.item || null;
  metalBinInput.value = metalBin.dataset.item || null;
  organicBinInput.value = organicBin.dataset.item || null;
});

for (const item of items) {
  item.addEventListener('dragstart', (e) => {
    // e.dataTransfer.dropEffect = 'link';
    draggedItem = e.target;
  });
}

for (const bin of bins) {
  bin.addEventListener('dragover', (e) => {
    e.preventDefault();
  });

  bin.addEventListener('drop', (e) => {
    e.preventDefault();

    if (isBinEmpty(bin)) {
      throwItem(draggedItem, bin);
    }

    draggedItem = null;
  });

  bin.addEventListener('click', () => {
    if (!isBinEmpty(bin)) {
      emptyBin(bin);
    }
  });
}

function isBinEmpty(bin) {
  return bin.classList.contains(EMPTY_BIN_CLASS);
}

function isItemThrown(item) {
  return item.classList.contains(THROWN_ITEM_CLASS);
}

function emptyBin(bin) {
  const itemId = bin.dataset.item;

  const item = getItemById(itemId);

  if (item) {
    unThrowItem(item, bin);
  }
}

function getItemById(itemId) {
  switch (itemId) {
    case BATTERY_ID:
      return battery;
    case APPLE_ID:
      return apple;
    case SODA_ID:
      return soda;
    default:
      return null;
  }
}

function throwItem(item, bin) {
  bin.classList.remove(EMPTY_BIN_CLASS);
  bin.dataset.item = item.id;

  item.classList.add(THROWN_ITEM_CLASS);
  item.removeAttribute('draggable');
}

function unThrowItem(item, bin) {
  bin.classList.add(EMPTY_BIN_CLASS);
  delete bin.dataset.item;

  item.classList.remove(THROWN_ITEM_CLASS);
  item.setAttribute('draggable', 'true');
}
