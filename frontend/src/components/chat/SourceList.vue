<template>

<div
    v-if="sources.length"
    class="sources"
>

<div class="title">

📚 引用来源

</div>

<div

v-for="source in sources"

:key="source.id"

class="source"

>

{{source.file_name}}

</div>

</div>

</template>

<script setup>

defineProps({

    sources:{

        type:Array,

        default:()=>[]

    }

})

</script>

<style scoped>

.sources{

    margin-top:12px;

    border-top:1px solid #444;

    padding-top:10px;

}

.source{

    margin-top:6px;

    font-size:13px;

}

.title{

    font-weight:bold;

}

</style>