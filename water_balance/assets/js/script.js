import $ from 'jquery'; // นำเข้า jQuery

$(document).ready(function () {
    // คำนวณความสูงของคอลัมน์ 1
    var column1Height = $('#colmap1').height();

    // กำหนดความสูงของ .square เท่ากับความสูงของคอลัมน์ 1
    $('.square').height(column1Height);
});
