// *************** show message *************** //
function showMessage(type, title, msg, delay) {
	Lobibox.notify(type, {
		delay: delay,
		title: title.toUpperCase(),
		msg: msg
	});
}

// *************** convert month to string *************** //
function getMonthString(month) {
    var month_ary = ["January", "Feburary", "March", "April", "May", "Jun", "July", "August", "September",
            "October", "November", "December"];
    if (month >= 1 && month <= 12)
        return month_ary[month-1];
    return "";
}

// *************** Generate Random String *************** //
function randomString(string_length) {
    /*Charecters you want to use for your Random String*/
    var chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
    var randomstring = '';

    for (var i = 0; i < string_length; i++) {
    var rnum = Math.floor(Math.random() * chars.length);
    randomstring += chars.substring(rnum, rnum + 1);
    }
    return randomstring;
}

// *************** Get Cookie *************** //
function getCooke(name) {
	var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// *************** Get CSRF Token *************** //
function getCsrfToken() {
	return getCooke("csrftoken");
}

// *************** Show Loading Gif *************** //
function showLoading() {
    $("#loading").css("display", "block");
}

// *************** Hide Loading Gif *************** //
function hideLoading() {
    $("#loading").css("display", "none");
}

// *************** Get Two Digits String *************** //
function getTwoDigitsStr(val) {
    if (val < 9)
        return "0" + val;
    return val;
}

FIRST_DELAY = 1000;

// *************** alert list *************** //
var alert_list = new Array();

// *************** 0x1....  Admin Panel *************** //
alert_list["0x10001"] = {
    "mode": "warning",
    "title": "Warning",
    "msg": "Please enter all information."
};

alert_list["0x10002"] = {
    "mode": "warning",
    "title": "Success",
    "msg": "Admin has been registered."
};

alert_list["0x10003"] = {
    "mode": "warning",
    "title": "Warning",
    "msg": "Email is already registered."
};

alert_list["0x10004"] = {
    "mode": "warning",
    "title": "Success",
    "msg": "Admin has been updated."
};

alert_list["0x10005"] = {
    "mode": "warning",
    "title": "Success",
    "msg": "Admin has been deleted."
};

alert_list["0x10006"] = {
    "mode": "warning",
    "title": "Success",
    "msg": "Agent has been registered."
};

alert_list["0x10007"] = {
    "mode": "warning",
    "title": "Warning",
    "msg": "Agent is already registered."
};

alert_list["0x10008"] = {
    "mode": "warning",
    "title": "Success",
    "msg": "Agent has been updated."
};

alert_list["0x10009"] = {
    "mode": "warning",
    "title": "Success",
    "msg": "Agent has been deleted."
};

alert_list["0x1000A"] = {
    "mode": "warning",
    "title": "Warning",
    "msg": "This menu name is already registered."
};

alert_list["0x1000B"] = {
    "mode": "warning",
    "title": "Warning",
    "msg": "Please select period type."
};

alert_list["0x1000C"] = {
    "mode": "warning",
    "title": "Warning",
    "msg": "Please enter Url."
};

alert_list["0x1000D"] = {
    "mode": "warning",
    "title": "Warning",
    "msg": "No agent is found."
};

alert_list["0x1000E"] = {
    "mode": "warning",
    "title": "Success",
    "msg": "Company has been registered."
};

alert_list["0x1000F"] = {
    "mode": "warning",
    "title": "Warning",
    "msg": "Company is already registered."
};

alert_list["0x10010"] = {
    "mode": "warning",
    "title": "Success",
    "msg": "Company has been updated."
};

alert_list["0x10011"] = {
    "mode": "warning",
    "title": "Success",
    "msg": "Company has been deleted."
};

alert_list["0x10012"] = {
    "mode": "warning",
    "title": "Success",
    "msg": "Advisor has been registered."
};

alert_list["0x10013"] = {
    "mode": "warning",
    "title": "Warning",
    "msg": "Advisor is already registered."
};

alert_list["0x10014"] = {
    "mode": "warning",
    "title": "Success",
    "msg": "Advisor has been updated."
};

alert_list["0x10015"] = {
    "mode": "warning",
    "title": "Success",
    "msg": "Advisor has been deleted."
};

alert_list["0x10016"] = {
    "mode": "warning",
    "title": "Warning",
    "msg": "Advisor can't have more than 3 buddies."
};

alert_list["0x10017"] = {
    "mode": "warning",
    "title": "Warning",
    "msg": "This name is already registered."
};

alert_list["0x10018"] = {
    "mode": "warning",
    "title": "Warning",
    "msg": "You need to enter country code for phone number as well. Ex; +12016143899"
};

alert_list["0x10019"] = {
    "mode": "warning",
    "title": "Warning",
    "msg": "This is in progress by another man now."
};

alert_list["0x1001A"] = {
    "mode": "warning",
    "title": "Warning",
    "msg": "This is already closed."
};

alert_list["0x1001B"] = {
    "mode": "warning",
    "title": "Success",
    "msg": "Done"
};

alert_list["0x1001C"] = {
    "mode": "warning",
    "title": "Warning",
    "msg": "Please enter text."
};

alert_list["0x1001D"] = {
    "mode": "warning",
    "title": "Warning",
    "msg": "Report should contain at least 10 words."
};

// *************** 0xF....  Others *************** //
alert_list["0xF0001"] = {
    "mode": "warning",
    "title": "Error",
    "msg": "Sorry, something went wrong."
};

