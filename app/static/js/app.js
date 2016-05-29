/**
 * Created by Andrew on 3/10/2016.
 */

$(document).ready(function () {
    var countdown = 11;
    var resets = 0; //Number of times the countdown was restarted on this question
    var currentQuestion = 0; // Links to the list  of questions by index - 0 is the starter question
    var currentCardStats = {view:0, time:0};
    var currentCard = {
        id: 'XXXXXX',
        totalResets: 0
    };
    var questions = [];

    function setCardClassOnPosition(position) {
        currentCardStats = {view:0, time:0};
        $(".question").removeClass('previous').removeClass('current').removeClass('next');
        if (position > 0) {
            $("#" + questions[position - 1].id).addClass('previous');
        }
        $("#" + questions[position].id).addClass('current');
        if (position < questions.length - 1) {
            $("#" + questions[position + 1].id).addClass('next');
        }
    }

    function nextQuestion() {
        questions[currentQuestion].views += currentCardStats.view;
        questions[currentQuestion].time += currentCardStats.time;

        currentQuestion = Math.min(++currentQuestion, questions.length - 1);
        setCardClassOnPosition(currentQuestion);
        console.log(questions[currentQuestion]);
    }

    function previousQuestion() {
        questions[currentQuestion].views += currentCardStats.view;
        questions[currentQuestion].time += currentCardStats.time;

        currentQuestion = Math.max(--currentQuestion, 0);
        setCardClassOnPosition(currentQuestion);
        console.log(questions[currentQuestion]);

    }

    !function () {
        currentCard.id = $('.card-body').attr('data-card-id');
        $("#questions").find('.question').each(function () {
            questions.push({id: this.id, views:0, time: 0})
        });
        currentQuestion = 0;
        setCardClassOnPosition(currentQuestion);
    }();


    var timer = Timer('#start-timer h3');

    $("button#start-timer").click(function () {
        currentCardStats.time += timer.start(countdown);
        currentCardStats.view = 1;
        console.log(currentCardStats);
    });

    $("button#next-question").click(function () {
        if (timer.isRunning() == true) {
            currentCardStats.time += timer.stop();
        }
        nextQuestion();

    });

    $("button#next-question-arrow").click(function () {
        if (timer.isRunning() == true) {
            currentCardStats.time += timer.stop();
        }
        nextQuestion();

    });

    $("button#previous-question-arrow").click(function () {
        if (timer.isRunning() == true) {
            currentCardStats.time += timer.stop();
        }
        previousQuestion();

    });

    $("button#submit-feedback").click(function() {
        console.log('/submit-feedback?card='+currentCard.id+'&question='+questions[currentQuestion].id);
        window.location.href='/submit-feedback?card='+currentCard.id+'&question='+questions[currentQuestion].id;
    })

});


function Timer(container) {
    //http://stackoverflow.com/questions/16134997/how-to-pause-and-resume-a-javascript-timer
    var startTime,
        seconds,
        remaining,
        on,
        ms,
        timer,
        obj,
        display = $(container),
        original_text = display.text();

    obj = {};
    obj.start = function (timerLength) {
        seconds = timerLength;
        obj.stop();
        ms = seconds * 1000;
        obj.resume();
        on = true;
        return seconds - remaining;
    };
    obj.resume = function () {
        startTime = new Date().getTime();
        timer = setInterval(obj.step, 250);
        on = true;
    };
    obj.stop = function () {
        clearInterval(timer);
        display.text(original_text);
        on = false;
        return seconds - remaining;
    };
    obj.pause = function () {
        ms = obj.step();
        clearInterval(timer);
        on = false;
    };
    obj.step = function () {
        var now = Math.max(0, ms - (new Date().getTime() - startTime));
        remaining = Math.floor(now / 1000) % 60;
        display.text(remaining);
        if (now == 0) {
            return obj.stop();
        }
        return now;
    };
    obj.isRunning = function () {
        return on
    };
    return obj;
}
