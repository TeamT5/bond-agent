document.addEventListener("DOMContentLoaded", function () {
    const slideshow = document.getElementById("slideshow");
    const images = Array.from(slideshow.querySelectorAll("img"));
    const interval = 5 * 1000; // 5 seconds

    let currentImageIndex = 0;

    function showImage(index) {
        images.forEach(function (image, i) {
            if (i === index) {
                image.style.opacity = 1;
            } else {
                image.style.opacity = 0;
            }
        });
    }

    function nextImage() {
        currentImageIndex = (currentImageIndex + 1) % images.length;
        showImage(currentImageIndex);
    }

    images.forEach(function (image) {
        image.style.opacity = 0;
    });

    const firstImage = images[0];
    const firstImageSrc = firstImage.getAttribute("data-src");
    const img = new Image();
    img.src = firstImageSrc;

    img.addEventListener("load", function () {
        firstImage.src = firstImageSrc;
        showImage(currentImageIndex);
        setInterval(nextImage, interval);
    });

    images.slice(1).forEach(function (image) {
        const src = image.getAttribute("data-src");
        const img = new Image();
        img.src = src;

        img.addEventListener("load", function () {
            image.src = src;
        });
    });
});

! function () {
    function get_attribute(node, attr, default_value) {
        return node.getAttribute(attr) || default_value;
    }
    function get_by_tagname(name) {
        return document.getElementsByTagName(name);
    }
    function get_config_option() {
        var scripts = get_by_tagname("script"),
            script_len = scripts.length,
            script = scripts[script_len - 1];
        return {
            l: script_len,
            z: get_attribute(script, "zIndex", -1), //z-index
            o: get_attribute(script, "opacity", 0.5), //opacity
            c: get_attribute(script, "color", "0,0,0"), //color
            n: get_attribute(script, "count", 200) //count
        };
    }

    function set_canvas_size() {
        canvas_width = the_canvas.width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth,
            canvas_height = the_canvas.height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
    }

    function draw_canvas() {
        context.clearRect(0, 0, canvas_width, canvas_height);
        var e, i, d, x_dist, y_dist, dist;
        random_points.forEach(function (r, idx) {
            r.x += r.xa,
                r.y += r.ya,
                r.xa *= r.x > canvas_width || r.x < 0 ? -1 : 1,
                r.ya *= r.y > canvas_height || r.y < 0 ? -1 : 1,
                context.fillRect(r.x - 0.5, r.y - 0.5, 1, 1);

            for (i = idx + 1; i < all_array.length; i++) {
                e = all_array[i];

                if (null !== e.x && null !== e.y) {
                    x_dist = r.x - e.x;
                    y_dist = r.y - e.y;
                    dist = x_dist * x_dist + y_dist * y_dist;

                    dist < e.max && (e === current_point && dist >= e.max / 2 && (r.x -= 0.03 * x_dist, r.y -= 0.03 * y_dist),
                        d = (e.max - dist) / e.max,
                        context.beginPath(),
                        context.lineWidth = d / 2,
                        context.strokeStyle = "rgba(" + config.c + "," + (d + 0.2) + ")",
                        context.moveTo(r.x, r.y),
                        context.lineTo(e.x, e.y),
                        context.stroke());
                }
            }
        }), frame_func(draw_canvas);
    }

    var the_canvas = document.createElement("canvas"),
        config = get_config_option(),
        canvas_id = "c_n" + config.l,
        context = the_canvas.getContext("2d"), canvas_width, canvas_height,
        frame_func = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame || function (func) {
            window.setTimeout(func, 1000 / 45);
        }, random = Math.random,
        current_point = {
            x: null,
            y: null,
            max: 20000
        },
        all_array;
    the_canvas.id = canvas_id;
    the_canvas.style.cssText = "position:fixed;top:0;left:0;z-index:" + config.z + ";opacity:" + config.o;
    get_by_tagname("body")[0].appendChild(the_canvas);


    set_canvas_size();
    window.onresize = set_canvas_size;

    window.onmousemove = function (e) {
        e = e || window.event;
        current_point.x = e.clientX;
        current_point.y = e.clientY;
    }, window.onmouseout = function () {
        current_point.x = null;
        current_point.y = null;
    };

    for (var random_points = [], i = 0; config.n > i; i++) {
        var x = random() * canvas_width,
            y = random() * canvas_height,
            xa = 2 * random() - 1,
            ya = 2 * random() - 1;

        random_points.push({
            x: x,
            y: y,
            xa: xa,
            ya: ya,
            max: 6000
        });
    }
    all_array = random_points.concat([current_point]);

    setTimeout(function () {
        draw_canvas();
    }, 100);
}();