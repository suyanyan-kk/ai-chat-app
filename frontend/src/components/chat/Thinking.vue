<template>

<div
    v-if="show"
    class="thinking"
>

🤔 正在思考...

</div>

</template>

<script setup>

defineProps({

    show:Boolean

})

</script>

<style scoped>

.thinking{

    font-size:13px;

    opacity:.65;

    margin-bottom:8px;

}

</style>