<template>
    <div class="flip-card">
        <div class="flip-card-inner">
            <div class="flip-card-front">
                <h3 style="margin-top:40%">
                    {{ this.front }}
                </h3>
            </div>
            <div class="flip-card-back">
                <h4 style="margin-top:30%">
                    {{ this.back }}
                </h4>
                <div class="form-check form-check-inline" style="margin-top:20%" id="difficulty-form">
                    <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1"
                        value="option1" @click="this.$emit('easy')">
                    <label class="form-check-label" for="inlineRadio1" style="color:green">Easy</label>
                    <br>
                    <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio2"
                        value="option2" @click="this.$emit('medium')">
                    <label class="form-check-label" for="inlineRadio2" style="color:orange">Medium</label>
                    <br>
                    <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio2"
                        value="option3" @click="this.$emit('hard')">
                    <label class="form-check-label" for="inlineRadio3" style="color:orangered">Hard</label>
                </div>
            </div>
        </div>
    </div>

</template>

<script>

export default {
    name: 'SingleCard',
    props: {
        front: String,
        back: String,
    },
    emits: ['easy', 'medium', 'hard']
}
</script>

<style>
* {
    border-radius: 2rem;
}

.flip-card {
    background-color: transparent;
    width: 300px;
    height: 300px;
    perspective: 1000px;
}

.flip-card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.6s;
    transform-style: preserve-3d;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}

.flip-card:hover .flip-card-inner {
    transform: rotateY(180deg);
}

.flip-card-front,
.flip-card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    -webkit-backface-visibility: hidden;
    backface-visibility: hidden;
}

.flip-card-front {
    background-color: whitesmoke;
    color: black;
}

.flip-card-back {
    background-color: #bbb;
    color: black;
    transform: rotateY(180deg);
}
</style>