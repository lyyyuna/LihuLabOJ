<template>
  <div>
    <navigation></navigation>
    <router-view></router-view>

  </div>
</template>

<script type="text/ecmascript-6">
  import navigation from "./components/navigation/navigation.vue";
  export default {

    components: {
      navigation,
    },

  };
</script>

<style>
.el-row {
    margin-bottom: 20px;
}
</style>
