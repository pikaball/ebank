const num=5;

function add(count)
{
	if (count==num) return 1;
	return count+1;
}

function change(now)
{
	if (now==1) return 2;
	return 1;
}

function imgpath(count)
{
	return 'url("../img/'+count+'.jpg")';
}

function chgid(now)
{
	return '#pic'+now;
}

var count=1;
var now=2;
function run()
{
	count=add(count);
	$(chgid(change(now))).css("background",imgpath(count));
	$(chgid(change(now))).css("background-size","cover");
	$(chgid(now)).fadeOut(1000);
	$(chgid(change(now))).fadeIn(1000);
	now=change(now);
}

setInterval(run,4000);