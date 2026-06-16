<template>

<div
    v-if="tool"
    class="tool-status"
>

🔧 正在调用

<b>{{tool}}</b>

...

</div>

</template>

<script setup>

defineProps({

    tool:String

})

</script>

<style scoped>

.tool-status{

    font-size:13px;

    margin-bottom:10px;

    color:#58a6ff;

}

</style>