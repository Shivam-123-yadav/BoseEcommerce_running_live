/**************************************** load more prodcuts script start ******************************/	
  $(document).ready(function(){
  $(".product").slice(0, 6).show();
  $("#loadMore").on("click", function(e){
    e.preventDefault();
    $(".product:hidden").slice(0, 6).slideDown();
    if($(".product:hidden").length == 0) {
      $("#loadMore").text("No Content").addClass("noContent");
    }
  });
  
})

/**************************************** load more prodcuts script end ******************************/	

/*--------------------------- product filter start -----------------------------------------------*/
	
 
	
	// Function to filter products
function filterProducts() {
    const searchInput = document.getElementById('searchBox').value.toLowerCase();
    const products = document.querySelectorAll('.product');
    products.forEach(product => {
        const productName = product.querySelector('.card-title').textContent.toLowerCase();
        if (productName.includes(searchInput)) {
            product.style.display = 'block';
        } else {
            product.style.display = 'none';
        }
    });
}

// Function to sort products by price
function sortProducts() {
    const sortBy = document.getElementById('sortByPrice').value;
    const products = document.getElementById('productsDisplay').querySelectorAll('.product');
    const sortedProducts = Array.from(products).sort((a, b) => {
        const priceA = parseFloat(a.querySelector('.boldprice').textContent.replace('Price: $', ''));
        const priceB = parseFloat(b.querySelector('.boldprice').textContent.replace('Price: $', ''));
        return sortBy === 'low' ? priceA - priceB : priceB - priceA;
    });
    const display = document.getElementById('productsDisplay');
    sortedProducts.forEach(product => {
        display.appendChild(product);
    });
}

// Function to show specified number of products
function showProducts() {
    const showCount = parseInt(document.getElementById('showProducts').value);
    const products = document.querySelectorAll('.product');
    let count = 0;
    products.forEach(product => {
        if (count < showCount) {
            product.style.display = 'block';
        } else {
            product.style.display = 'none';
        }
        count++;
    });
}

// Function to change between grid and list view
function changeView(viewType) {
    const display = document.getElementById('productsDisplay');
    if (viewType === 'list') {
        display.classList.remove('grid');
        display.classList.add('list');
    } else {
        display.classList.remove('list');
        display.classList.add('grid');
    }
}
		
		function filterProductsColor() {
    const searchInput = document.getElementById('searchBox').value.toLowerCase();
    const colorCheckboxes = document.querySelectorAll('#colorFilters input[type="checkbox"]');
    const products = document.querySelectorAll('.product');
    products.forEach(product => {
        const productName = product.querySelector('.card-title').textContent.toLowerCase();
        const productColor = product.dataset.color.toLowerCase();
        const selectedColors = Array.from(colorCheckboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.value.toLowerCase());
        if ((productName.includes(searchInput) || searchInput === '') && (selectedColors.includes(productColor) || selectedColors.length === 0)) {
            product.style.display = 'block';
        } else {
            product.style.display = 'none';
        }
    });
}

	
 
	
/*--------------------------- product filter end -----------------------------------------------*/




/**************************** product price range slider start ***************************************/

const rangeInput = document.querySelectorAll(".range-input input"),
priceInput = document.querySelectorAll(".price-input input"),
range = document.querySelector(".slider .progress");
let priceGap = 1000;

priceInput.forEach(input =>{
    input.addEventListener("input", e =>{
        let minPrice = parseInt(priceInput[0].value),
        maxPrice = parseInt(priceInput[1].value);
        
        if((maxPrice - minPrice >= priceGap) && maxPrice <= rangeInput[1].max){
            if(e.target.className === "input-min"){
                rangeInput[0].value = minPrice;
                range.style.left = ((minPrice / rangeInput[0].max) * 100) + "%";
            }else{
                rangeInput[1].value = maxPrice;
                range.style.right = 100 - (maxPrice / rangeInput[1].max) * 100 + "%";
            }
        }
    });
});

rangeInput.forEach(input =>{
    input.addEventListener("input", e =>{
        let minVal = parseInt(rangeInput[0].value),
        maxVal = parseInt(rangeInput[1].value);

        if((maxVal - minVal) < priceGap){
            if(e.target.className === "range-min"){
                rangeInput[0].value = maxVal - priceGap
            }else{
                rangeInput[1].value = minVal + priceGap;
            }
        }else{
            priceInput[0].value = minVal;
            priceInput[1].value = maxVal;
            range.style.left = ((minVal / rangeInput[0].max) * 100) + "%";
            range.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
        }
    });
});


/**************************** product price range slider end ***************************************/

jQuery(function ($) {
  "use strict";
  var $window = $(window);
  var $root = $("html, body");

  /* ----- Back to Top ----- */
  $("body").append('<a href="#" class="back-top"><i class="fa fa-angle-up"></i></a>');
  var amountScrolled = 700;
  var backBtn = $("a.back-top");
  $window.on("scroll", function () {
    if ($window.scrollTop() > amountScrolled) {
      backBtn.addClass("back-top-visible");
    } else {
      backBtn.removeClass("back-top-visible");
    }
  });
  backBtn.on("click", function () {
    $root.animate({
      scrollTop: 0
    }, 700);
    return false;
  });
	
	

  /* service page banner slider start */
  function slider(flag, num) {
    var current = $(".item.current"),
      next,
      index;
    if (!flag) {
      next = current.is(":last-child") ? $(".item").first() : current.next();
      index = next.index();
    } else if (flag === 'dot') {
      next = $(".item").eq(num);
      index = num;
    } else {
      next = current.is(":first-child") ? $(".item").last() : current.prev();
      index = next.index();
    }
    next.addClass("current");
    current.removeClass("current");
    $(".dot").eq(index).addClass("current").siblings().removeClass("current");
  }
  var setSlider = setInterval(slider, 4000);

  $(".button").on("click", function () {
    clearInterval(setSlider);
    var flag = $(this).is(".prev") ? true : false;
    slider(flag);
    setSlider = setInterval(slider, 4000);
  });

  $(".dot").on("click", function () {
    if ($(this).is(".current")) return;
    clearInterval(setSlider);
    var num = $(this).index();
    slider('dot', num);
    setSlider = setInterval(slider, 4000);
  });

  /* service page banner slider end */


  

  $(".banner-slider").slick({
    infinite: true,
    autoplay: true,
    rows: 1,
    autoplaySpeed: 4000,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 2,
    dots: true,
    pauseOnHover: false,
    arrows: false,
    adaptiveHeight: true,
    cssEase: 'linear',
    swipeToSlide: true,
    responsive: [{
        breakpoint: 1024,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 2,
          dots: true,
          arrows: false,
        }
      },

      {
        breakpoint: 768,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 2,
          arrows: false,
          dots: true,
        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 2,
          dots: true,
          arrows: false,
        }
      },
    ]
  });
	
	
	
	
	$(".customerfeedback-slider").slick({
    infinite: false,
    autoplay: false,
    rows: 1,
    autoplaySpeed: 4000,
    speed: 500,
    slidesToShow: 2,
    slidesToScroll: 2,
    dots: true,
    pauseOnHover: false,
    arrows: true,
    adaptiveHeight: true,
    cssEase: 'linear',
    swipeToSlide: true,
    responsive: [{
        breakpoint: 1024,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 2,
          dots: true,
          arrows: false,
        }
      },

      {
        breakpoint: 768,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 2,
          arrows: false,
          dots: true,
        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 2,
          dots: true,
          arrows: false,
        }
      },
    ]
  });

	 
   

  $('[data-fancybox]').fancybox({
    youtube: {
      controls: 0,
      showinfo: 0
    },
    vimeo: {
      color: 'f00'
    }
  });

  $("#showbtech").click(function () {
    $(".btechbox").show();
  });
  $(".close-container").click(function () {
    $(".btechbox").hide();
  });


  $("#showscience").click(function () {
    $(".sciencebox").show();
  });
  $(".close-container").click(function () {
    $(".sciencebox").hide();
  });

  $("#showlaw").click(function () {
    $(".lawbox").show();
  });
  $(".close-container").click(function () {
    $(".lawbox").hide();
  });

  $("#showmgmt").click(function () {
    $(".mgmtbox").show();
  });
  $(".close-container").click(function () {
    $(".mgmtbox").hide();
  });

});
