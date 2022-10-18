<template>
  <div class="archive left">
    <el-timeline>
      <el-timeline-item v-for="(l, i) in state.articlesList" :key="l.year" hide-timestamp placement="top">
        <h3 class="year">{{ l.year }}</h3>
        <el-timeline-item
            v-for="(item, index) in l.list"
            :key="item.id"
            hide-timestamp
            placement="top"
        >
          <router-link :to="`/article/?id=${item.id}`" target="_blank">
            <h3 class="title">{{ item.title }}</h3>
          </router-link>
          <p>{{ formatTime(item.created_at) }}</p>
        </el-timeline-item>
      </el-timeline-item>
    </el-timeline>
  </div>
</template>
<script lang="ts">
import {defineComponent, onMounted, reactive} from "vue";
import {timestampToTime} from "../../utils";
import {ArticleArchiveList, PageInfo} from "../../types";
import {getArchiveList} from "../../api/service";
import {useStore} from "vuex";
import {SET_NAV_INDEX_BY_ROUTE, StateKey} from "../../store";


export default defineComponent({
  name: "Archive",
  setup() {
    const state = reactive({
      isLoadEnd: false,
      isLoading: false,
      articlesList: [] as Array<ArticleArchiveList>,
      total: 0,
      params: {
        page: 1,
        page_size: 10,
      } as PageInfo
    });

    const formatTime = (value: string | Date): string => {
      return timestampToTime(value, true);
    }

    const handleSearch = async (): Promise<void> => {
      state.isLoading = true;
      const params: PageInfo = state.params
      try {
        const data: any = await getArchiveList(params)
        state.isLoading = false;
        state.articlesList = [...state.articlesList, ...data.results];
        state.total = data.count;
        state.params.page++;
        if (state.total === state.articlesList.length) {
          state.isLoadEnd = true;
        }
      } catch (e) {
        state.isLoading = false;
      }

    }

    onMounted(() => {
      const store = useStore(StateKey)
      store.dispatch(SET_NAV_INDEX_BY_ROUTE, '/archive')
      handleSearch();
    })

    return {
      state,
      formatTime,
      handleSearch
    };
  },
})
;
</script>

<style lang="less" scoped>
.archive {
  padding: 40px 0;

  .year {
    font-size: 30px;
    font-weight: bold;
    color: #000;
    margin-top: 0;
  }

  a {
    text-decoration: none;
  }

  .title {
    color: #333;

    &:hover {
      color: #1890ff;
    }
  }
}
</style>

