<template>
  <div id="app">
    <div>
    <router-view v-if="isRouterAlive"></router-view>
    </div>
    <!-- <router-view /> -->

  </div>
</template>

<script>
export default {
  name: "app",
  data() {
    return {
      isRouterAlive: true,
    };
  },
  provide() {
    //提供
    return {
      reload: this.reload,
    };
  },
  methods: {
    reload() {
      this.isRouterAlive = false;
      this.$nextTick(function () {
        this.isRouterAlive = true;
      });
    },
  },
};
</script>
