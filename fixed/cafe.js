// One source of truth for every fact on the site.
// Change a price or the hours here and every page updates.
const CAFE = {
  name: "BTech Cafe Walla",
  location: "Near UPES campus, Bidholi, Dehradun",
  hours: "Every day, 8 AM to 11 PM",
  open: "08:00",
  lastOrder: "22:45",
  menu: [
    {
      section: "Chai & coffee",
      items: [
        { id: "cutting", name: "Cutting chai", price: 15, veg: true, contains: ["milk"] },
        { id: "masala", name: "Masala chai", price: 25, veg: true, contains: ["milk"] },
        { id: "black", name: "Black coffee", price: 40, veg: true, contains: [] },
        { id: "cold", name: "Cold coffee", price: 70, veg: true, contains: ["milk"] },
      ],
    },
    {
      section: "Maggi & snacks",
      items: [
        { id: "maggi", name: "Plain Maggi", price: 40, veg: true, contains: ["gluten"] },
        { id: "cheesemaggi", name: "Cheese Maggi", price: 60, veg: true, contains: ["gluten", "milk"] },
        { id: "momos", name: "Veg momos (6)", price: 60, veg: true, contains: ["gluten", "soy"] },
        { id: "bunmaska", name: "Bun maska", price: 30, veg: true, contains: ["gluten", "milk"] },
      ],
    },
    {
      section: "Sandwiches",
      items: [
        { id: "vegsand", name: "Veg grilled sandwich", price: 60, veg: true, contains: ["gluten", "milk"] },
        { id: "paneer", name: "Paneer tikka sandwich", price: 90, veg: true, contains: ["gluten", "milk"] },
        { id: "egg", name: "Egg bhurji sandwich", price: 70, veg: false, contains: ["gluten", "egg", "milk"] },
      ],
    },
    {
      section: "Something sweet",
      items: [
        { id: "brownie", name: "Walnut brownie", price: 60, veg: false, contains: ["gluten", "milk", "egg", "tree nuts"] },
        { id: "hotchoc", name: "Hot chocolate", price: 80, veg: true, contains: ["milk"] },
      ],
    },
  ],
};

const rupees = (n) => "₹" + n.toLocaleString("en-IN");

// Fill every [data-cafe="..."] element with the matching fact.
document.querySelectorAll("[data-cafe]").forEach((el) => {
  el.textContent = CAFE[el.dataset.cafe];
});

// Mark the current page in the nav for screen readers and styling.
const here = location.pathname.split("/").pop() || "index.html";
document.querySelectorAll(".nav a").forEach((a) => {
  if (a.getAttribute("href") === here) a.setAttribute("aria-current", "page");
});

document.querySelectorAll("[data-year]").forEach((el) => {
  el.textContent = new Date().getFullYear();
});
