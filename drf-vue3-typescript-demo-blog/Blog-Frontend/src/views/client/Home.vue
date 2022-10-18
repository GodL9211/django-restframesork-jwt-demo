<template>
  <div class="left clearfix">
    <h3 v-if="state.params.tags" class="left-title">
      {{ state.tag_name }} 相关的文章：
    </h3>
    <ArticleList :article-list="state.articlesList" />
    <Loading v-if="state.isLoading"></Loading>
    <EndLoading v-if="state.isLoadEnd"></EndLoading>
  </div>
</template>

<script lang="ts">
import { defineComponent, nextTick, onMounted, reactive } from "vue";
import {
  getDocumentHeight,
  getQueryStringByName,
  getScrollTop,
  getWindowHeight,
  throttle,
} from "../../utils";
import EndLoading from "../../components/EndLoading.vue";
import Loading from "../../components/Loading.vue";
import { Article, ArticleArray, ArticleParams } from "../../types";
import { getArticleList } from "../../api/service";
import ArticleList from "../../components/ArticleList.vue";

const viewHeight = window.innerHeight || document.documentElement.clientHeight;
const lazyload = throttle(() => {
  const imgs = document.querySelectorAll("#list .item img");
  let num = 0;
  for (let i = num; i < imgs.length; i++) {
    let distance = viewHeight - imgs[i].getBoundingClientRect().top;
    let imgItem: any = imgs[i];
    if (distance >= 100) {
      let hasLaySrc = imgItem.getAttribute("data-has-lazy-src");
      if (hasLaySrc === "false") {
        imgItem.src = imgItem.getAttribute("data-src");
        imgItem.setAttribute("data-has-lazy-src", "true");
      }
      num = i + 1;
    }
  }
}, 1000);

export default defineComponent({
  name: "Home",
  components: {
    ArticleList,
    EndLoading,
    Loading,
  },
  watch: {
    "$store.state.articleParams": {
      handler(val: any, oldVal: any) {
        this.state.params.tags = val.tags;
        this.state.params.catalog = val.catalog;
        this.state.articlesList = [];
        this.state.params.page = 1;
        this.handleSearch();
      },
    },
  },
  setup() {
    const state = reactive({
      isLoadEnd: false,
      isLoading: false,
      articlesList: [] as Array<Article>,
      total: 0,
      tag_name: decodeURI(getQueryStringByName("tag_name")),
      params: {
        title: undefined,
        tags: undefined,
        catalog: undefined,
        page: 1,
        page_size: 10,
      } as ArticleParams,
    });

    const handleSearch = async (): Promise<void> => {
      state.isLoading = true;

      try {
        const data: ArticleArray = await getArticleList(state.params);
        state.isLoading = false;
        state.articlesList = [...state.articlesList, ...data.results];
        state.total = data.count;
        state.params.page++;
        await nextTick(() => {
          lazyload();
        });
        if (
          data.results.length === 0 ||
          state.total === state.articlesList.length
        ) {
          state.isLoadEnd = true;
          document.removeEventListener("scroll", () => {});
          window.onscroll = null;
        }
      } catch (e) {
        console.error(e);
        state.isLoading = false;
      }
    };

    onMounted(() => {
      window.onscroll = () => {
        if (getScrollTop() + getWindowHeight() > getDocumentHeight() - 100) {
          if (state.isLoadEnd === false && state.isLoading === false) {
            console.info("222");
            handleSearch();
          }
        }
      };
      document.addEventListener("scroll", lazyload);
      handleSearch();
    });

    return {
      state,
      handleSearch,
    };
  },
});
</script>


<style lang="less">
a {
  text-decoration: none;
}
</style>