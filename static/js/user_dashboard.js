$(function () {
  "use strict";

  $(".js-menu-toggle").click(function (e) {
    var $this = $(this);

    if ($("body").hasClass("show-sidebar")) {
      $("body").removeClass("show-sidebar");
      $this.removeClass("active");
    } else {
      $("body").addClass("show-sidebar");
      $this.addClass("active");
    }

    e.preventDefault();
  });

  // click outisde offcanvas
  $(document).mouseup(function (e) {
    var container = $(".sidebar");
    if (!container.is(e.target) && container.has(e.target).length === 0) {
      if ($("body").hasClass("show-sidebar")) {
        $("body").removeClass("show-sidebar");
        $("body").find(".js-menu-toggle").removeClass("active");
      }
    }
  });

  // click on the sidebar
  $(".home").click(function (e) {
    var $this = $(this);
    if (!$(".home").hasClass("active")) {
      $this.addClass("active");
    }
    $(".explore").removeClass("active");
    $(".notifications").removeClass("active");
    $(".stats").removeClass("active");
    $(".signout").removeClass("active");
    $(".records").removeClass("active");
  });

  $(".explore").click(function (e) {
    var $this = $(this);
    if (!$(".explore").hasClass("active")) {
      $this.addClass("active");
    }
    $(".home").removeClass("active");
    $(".notifications").removeClass("active");
    $(".stats").removeClass("active");
    $(".signout").removeClass("active");
    $(".records").removeClass("active");
  });

  $(".notifications").click(function (e) {
    var $this = $(this);
    if (!$(".notifications").hasClass("active")) {
      $this.addClass("active");
    }
    $(".explore").removeClass("active");
    $(".home").removeClass("active");
    $(".stats").removeClass("active");
    $(".signout").removeClass("active");
    $(".records").removeClass("active");
  });

  $(".stats").click(function (e) {
    var $this = $(this);
    if (!$(".stats").hasClass("active")) {
      $this.addClass("active");
    }
    $(".explore").removeClass("active");
    $(".notifications").removeClass("active");
    $(".home").removeClass("active");
    $(".records").removeClass("active");
    $(".signout").removeClass("active");
  });

  $(".records").click(function (e) {
    var $this = $(this);
    if (!$(".records").hasClass("active")) {
      $this.addClass("active");
    }
    $(".explore").removeClass("active");
    $(".notifications").removeClass("active");
    $(".home").removeClass("active");
    $(".status").removeClass("active");
    $(".signout").removeClass("active");
  });

  $(".signout").click(function (e) {
    var $this = $(this);
    if (!$(".home").hasClass("active")) {
      $this.addClass("active");
    }
    $(".explore").removeClass("active");
    $(".notifications").removeClass("active");
    $(".stats").removeClass("active");
    $(".home").removeClass("active");
    $(".records").removeClass("active");
  });
});

// checkbox = document.getElementById('check-test');

// checkbox.addEventListener('change', e => {

//     if(e.target.checked){
// 		console.log('Bye');
// 		document.getElementById('tests').required = true;
//     }
//     else{
// 		console.log('Hello');
//         document.getElementById('tests').required = false;
//     }

// });

// const btn = document.querySelector("#btn-submit");
// btn.onclick = function () {
//   const rbs = document.querySelectorAll('input[name="lab-type"]');
//   let selectedValue;
//   for (const rb of rbs) {
//     if (rb.checked) {
//       selectedValue = rb.value;
//       break;
//     }
//   }
//   if (selectedValue.match("pathology")) {
//     document.getElementById("pathology-section").style.display = "block";
//     document.getElementById("radiology-section").style.display = "none";
//     document.getElementById("pharmacy-section").style.display = "none";
//     document.getElementById("select-section").style.display = "none";
//   } else if (selectedValue.match("radiology")) {
//     document.getElementById("radiology-section").style.display = "block";
//     document.getElementById("pathology-section").style.display = "none";
//     document.getElementById("pharmacy-section").style.display = "none";
//     document.getElementById("select-section").style.display = "none";
//   } else if (selectedValue.match("pharmacy")) {
//     document.getElementById("pharmacy-section").style.display = "block";
//     document.getElementById("pathology-section").style.display = "none";
//     document.getElementById("radiology-section").style.display = "none";
//     document.getElementById("select-section").style.display = "none";
//   } else {
//     document.getElementById("select-section").style.display = "block";
//     document.getElementById("radiology-section").style.display = "none";
//     document.getElementById("pharmacy-section").style.display = "none";
//     document.getElementById("pathology-section").style.display = "none";
//   }
// };

const btn1 = document.querySelector("#btn-pharma");
btn1.onclick = function () {
  const rbs = document.querySelectorAll('input[name="pharmatype"]');
  let selectedValue;
  for (const rb of rbs) {
    if (rb.checked) {
      selectedValue = rb.value;
      break;
    }
  }
  if (selectedValue.match("stock")) {
    document.getElementById("new-stock-section").style.display = "block";
    document.getElementById("new-dispense-section").style.display = "none";
    document.getElementById("pharma-type-section").style.display = "none";
    text - indigo - 500, border - indigo - 500;
  } else if (selectedValue.match("dispense")) {
    document.getElementById("new-dispense-section").style.display = "block";
    document.getElementById("new-stock-section").style.display = "none";
    document.getElementById("pharma-type-section").style.display = "none";
  } else {
    document.getElementById("pharma-type-section").style.display = "block";
    document.getElementById("new-stock-section").style.display = "none";
    document.getElementById("new-dispense-sectionn").style.display = "none";
  }
};

function change_detail() {
  document.getElementById("desc_a").onclick = function () {
    document.getElementById("desc").style.display = "block";
    document.getElementById("review").style.display = "none";
    document.getElementById("details").style.display = "none";
    document.getElementById("desc_a").classList.add("text-indigo-500");
    document.getElementById("desc_a").classList.add("border-indigo-500");
    document.getElementById("rev_a").classList.remove("text-indigo-500");
    document.getElementById("rev_a").classList.remove("border-indigo-500");
    document.getElementById("det_a").classList.remove("text-indigo-500");
    document.getElementById("det_a").classList.remove("border-indigo-500");
  };

  document.getElementById("rev_a").onclick = function () {
    document.getElementById("review").style.display = "block";
    document.getElementById("desc").style.display = "none";
    document.getElementById("details").style.display = "none";
    document.getElementById("rev_a").classList.add("text-indigo-500");
    document.getElementById("rev_a").classList.add("border-indigo-500");
    document.getElementById("desc_a").classList.add("border-gray-300");
    document.getElementById("desc_a").classList.remove("text-indigo-500");
    document.getElementById("desc_a").classList.remove("border-indigo-500");
    document.getElementById("det_a").classList.remove("text-indigo-500");
    document.getElementById("det_a").classList.remove("border-indigo-500");
  };

  document.getElementById("det_a").onclick = function () {
    document.getElementById("details").style.display = "block";
    document.getElementById("desc").style.display = "none";
    document.getElementById("review").style.display = "none";
    document.getElementById("det_a").classList.add("text-indigo-500");
    document.getElementById("det_a").classList.add("border-indigo-500");
    document.getElementById("desc_a").classList.add("border-gray-300");
    document.getElementById("rev_a").classList.remove("text-indigo-500");
    document.getElementById("rev_a").classList.remove("border-indigo-500");
    document.getElementById("desc_a").classList.remove("text-indigo-500");
    document.getElementById("desc_a").classList.remove("border-indigo-500");
  };
}

function change_detail1() {
  document.getElementById("obvs_a").onclick = function () {
    document.getElementById("obvs").style.display = "block";
    document.getElementById("impr").style.display = "none";
    document.getElementById("obvs_a").classList.add("text-indigo-500");
    document.getElementById("obvs_a").classList.add("border-indigo-500");
    document.getElementById("impr_a").classList.remove("text-indigo-500");
    document.getElementById("impr_a").classList.remove("border-indigo-500");
  };

  document.getElementById("impr_a").onclick = function () {
    document.getElementById("impr").style.display = "block";
    document.getElementById("obvs").style.display = "none";
    document.getElementById("impr_a").classList.add("text-indigo-500");
    document.getElementById("impr_a").classList.add("border-indigo-500");
    document.getElementById("obvs_a").classList.add("border-gray-300");
    document.getElementById("obvs_a").classList.remove("text-indigo-500");
    document.getElementById("obvs_a").classList.remove("border-indigo-500");
  };
 
}


function display_stock(){

  console.log('Stock');
  let elems = document.getElementsByClassName('Pharmacy-New Stock');
  for (var i=0;i<elems.length;i+=1){
    elems[i].classList.add('table-row');
    elems[i].classList.remove('hidden');
  };
  let elems1 = document.getElementsByClassName('Pharmacy-Dispatched');
  for (var i=0;i<elems1.length;i+=1){
    elems1[i].classList.add('hidden');
    elems1[i].classList.remove('table-row');
  };
};

function display_disp(){
  
  let elems = document.getElementsByClassName('Pharmacy-New Stock');
  for (var i=0;i<elems.length;i+=1){
    elems[i].classList.add('hidden');
    elems[i].classList.remove('table-row');
  };
  let elems1 = document.getElementsByClassName('Pharmacy-Dispatched');
  for (var i=0;i<elems1.length;i+=1){
    elems1[i].classList.add('table-row');
    elems1[i].classList.remove('hidden');
  };
};

function display_all_stock(){
  
  let elems = document.getElementsByClassName('Pharmacy-New Stock');
  for (var i=0;i<elems.length;i+=1){
    elems[i].classList.remove('hidden');
    elems[i].classList.add('table-row');
  };
  let elems1 = document.getElementsByClassName('Pharmacy-Dispatched');
  for (var i=0;i<elems1.length;i+=1){
    elems1[i].classList.add('table-row');
    elems1[i].classList.remove('hidden');
  };
};

function display_appointment(){

 
  let elems = document.getElementsByClassName('Appointment');
  for (var i=0;i<elems.length;i+=1){
    // elems[i].classList.add('table-row');
    elems[i].classList.remove('hidden');
  };
  let elems1 = document.getElementsByClassName('Radiology/Ultrasound');
  for (var i=0;i<elems1.length;i+=1){
    elems1[i].classList.add('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems2 = document.getElementsByClassName('Pharmacy');
  for (var i=0;i<elems2.length;i+=1){
    elems2[i].classList.add('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems3 = document.getElementsByClassName('Pathology');
  for (var i=0;i<elems3.length;i+=1){
    elems3[i].classList.add('hidden');
    // elems1[i].classList.remove('table-row');
  };
};

function display_pharmacy(){

  
  let elems = document.getElementsByClassName('Appointment');
  for (var i=0;i<elems.length;i+=1){
    // elems[i].classList.add('table-row');
    elems[i].classList.add('hidden');
  };
  let elems1 = document.getElementsByClassName('Radiology/Ultrasound');
  for (var i=0;i<elems1.length;i+=1){
    elems1[i].classList.add('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems2 = document.getElementsByClassName('Pharmacy');
  for (var i=0;i<elems2.length;i+=1){
    elems2[i].classList.remove('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems3 = document.getElementsByClassName('Pathology');
  for (var i=0;i<elems3.length;i+=1){
    elems3[i].classList.add('hidden');
    // elems1[i].classList.remove('table-row');
  };
};

function display_laboratry(){

  
  let elems = document.getElementsByClassName('Appointment');
  for (var i=0;i<elems.length;i+=1){
    // elems[i].classList.add('table-row');
    elems[i].classList.add('hidden');
  };
  let elems1 = document.getElementsByClassName('Radiology/Ultrasound');
  for (var i=0;i<elems1.length;i+=1){
    elems1[i].classList.remove('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems2 = document.getElementsByClassName('Pharmacy');
  for (var i=0;i<elems2.length;i+=1){
    elems2[i].classList.add('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems3 = document.getElementsByClassName('Pathology');
  for (var i=0;i<elems3.length;i+=1){
    elems3[i].classList.remove('hidden');
    // elems1[i].classList.remove('table-row');
  };
};

function display_all(){

  
  let elems = document.getElementsByClassName('Appointment');
  for (var i=0;i<elems.length;i+=1){
    // elems[i].classList.add('table-row');
    elems[i].classList.remove('hidden');
  };
  let elems1 = document.getElementsByClassName('Radiology/Ultrasound');
  for (var i=0;i<elems1.length;i+=1){
    elems1[i].classList.remove('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems2 = document.getElementsByClassName('Pharmacy');
  for (var i=0;i<elems2.length;i+=1){
    elems2[i].classList.remove('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems3 = document.getElementsByClassName('Pathology');
  for (var i=0;i<elems3.length;i+=1){
    elems3[i].classList.remove('hidden');
    // elems1[i].classList.remove('table-row');
  };
};


function display_mri(){

  let elems = document.getElementsByClassName('MRI');
  for (var i=0;i<elems.length;i+=1){
    // elems[i].classList.add('table-row');
    elems[i].classList.remove('hidden');
  };
  let elems1 = document.getElementsByClassName('CT-Scan');
  for (var i=0;i<elems1.length;i+=1){
    elems1[i].classList.add('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems2 = document.getElementsByClassName('X-Ray');
  for (var i=0;i<elems2.length;i+=1){
    elems2[i].classList.add('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems3 = document.getElementsByClassName('UltraSound');
  for (var i=0;i<elems3.length;i+=1){
    elems3[i].classList.add('hidden');
    // elems1[i].classList.remove('table-row');
  };
};
function display_ctscan(){

  let elems = document.getElementsByClassName('MRI');
  for (var i=0;i<elems.length;i+=1){
    // elems[i].classList.add('table-row');
    elems[i].classList.add('hidden');
  };
  let elems1 = document.getElementsByClassName('CT-Scan');
  for (var i=0;i<elems1.length;i+=1){
    elems1[i].classList.remove('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems2 = document.getElementsByClassName('X-Ray');
  for (var i=0;i<elems2.length;i+=1){
    elems2[i].classList.add('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems3 = document.getElementsByClassName('UltraSound');
  for (var i=0;i<elems3.length;i+=1){
    elems3[i].classList.add('hidden');
    // elems1[i].classList.remove('table-row');
  };
};

function display_xray(){

  let elems = document.getElementsByClassName('MRI');
  for (var i=0;i<elems.length;i+=1){
    // elems[i].classList.add('table-row');
    elems[i].classList.add('hidden');
  };
  let elems1 = document.getElementsByClassName('CT-Scan');
  for (var i=0;i<elems1.length;i+=1){
    elems1[i].classList.add('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems2 = document.getElementsByClassName('X-Ray');
  for (var i=0;i<elems2.length;i+=1){
    elems2[i].classList.remove('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems3 = document.getElementsByClassName('UltraSound');
  for (var i=0;i<elems3.length;i+=1){
    elems3[i].classList.add('hidden');
    // elems1[i].classList.remove('table-row');
  };
};

function display_ultra(){

  let elems = document.getElementsByClassName('MRI');
  for (var i=0;i<elems.length;i+=1){
    // elems[i].classList.add('table-row');
    elems[i].classList.add('hidden');
  };
  let elems1 = document.getElementsByClassName('CT-Scan');
  for (var i=0;i<elems1.length;i+=1){
    elems1[i].classList.add('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems2 = document.getElementsByClassName('X-Ray');
  for (var i=0;i<elems2.length;i+=1){
    elems2[i].classList.add('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems3 = document.getElementsByClassName('UltraSound');
  for (var i=0;i<elems3.length;i+=1){
    elems3[i].classList.remove('hidden');
    // elems1[i].classList.remove('table-row');
  };
};


function display_all_rad(){

  let elems = document.getElementsByClassName('MRI');
  for (var i=0;i<elems.length;i+=1){
    // elems[i].classList.add('table-row');
    elems[i].classList.remove('hidden');
  };
  let elems1 = document.getElementsByClassName('CT-Scan');
  for (var i=0;i<elems1.length;i+=1){
    elems1[i].classList.remove('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems2 = document.getElementsByClassName('X-Ray');
  for (var i=0;i<elems2.length;i+=1){
    elems2[i].classList.remove('hidden');
    // elems1[i].classList.remove('table-row');
  };
  let elems3 = document.getElementsByClassName('UltraSound');
  for (var i=0;i<elems3.length;i+=1){
    elems3[i].classList.remove('hidden');
    // elems1[i].classList.remove('table-row');
  };
};