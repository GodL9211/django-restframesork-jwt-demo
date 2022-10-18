<template>
  <div class="comment-list">
    <div class="top-title">
      <span>{{ numbers }} 条评论</span>
    </div>
    <div v-for="(item, i) in state.comments" :key="item.id" class="item">
      <div class="item-header">
        <div class="author">
          <div class="avatar">
            <img
              v-if="!item.user_info.avatar"
              alt="默认图片"
              src="../assets/user.png"
            />
            <img v-else :src="item.user_info.avatar" alt="" />
          </div>
        </div>
        <div class="info">
          <div class="name">
            {{ item.user_info.name
            }}{{ item.user_info.role === "Admin" ? "(作者)" : "" }}
          </div>
          <div class="time">{{ formatTime(item.created_at) }}</div>
        </div>
      </div>
      <div class="comment-detail">{{ item.content }}</div>
      <div class="item-comment">
        <div
          class="message"
          @click="showCommentModal(item.id, item.user_info.id)"
        >
          <el-button size="small">回复</el-button>
        </div>
      </div>
      <div v-for="e in item.comment_replies" :key="e._id" class="item-other">
        <div class="item-header">
          <div class="author">
            <div class="avatar">
              <img
                v-if="!e.user_info.avatar"
                alt="默认图片"
                src="../assets/user.png"
              />
              <img v-else :src="e.user_info.avatar" alt="" />
            </div>
          </div>
          <div class="info">
            <div class="name">
              {{ e.user_info.name }}
              {{ e.user_info.role === "Admin" ? "(作者)" : "" }}
            </div>
            <div class="time">
              {{ formatTime(e.created_at) }}
            </div>
          </div>
        </div>
        <div class="comment-detail">
          {{ e.content }}
        </div>
      </div>
    </div>
    <Comment
      :article_id="article_id"
      :forArticle="false"
      :reply="state.comment_id"
      :show-dialog="state.visible"
      @cancel="handleCancel"
      @ok="handleOk"
    />
  </div>
</template>

<script lang="ts">
import { ElMessage } from "element-plus";
import {
  defineAsyncComponent,
  defineComponent,
  onMounted,
  reactive,
} from "vue";
import { timestampToTime } from "../utils";
import { CommentInfo } from "../types";
import { getArticleComments } from "../api/service";

export default defineComponent({
  name: "CommentList",
  components: {
    Comment: defineAsyncComponent(() => import("./Comment.vue")),
  },
  props: {
    numbers: {
      type: Number,
      default: 0,
    },
    article_id: {
      type: Number,
      default: undefined,
    },
  },

  setup(props, context) {
    const state = reactive({
      visible: false,
      comment_id: 0,
      comments: [] as Array<CommentInfo>,
      reply: 0,
    });

    const formatTime = (value: string | Date): string => {
      return timestampToTime(value, true);
    };

    const handleCancel = (): void => {
      state.visible = false;
    };

    const getCommentList = async () => {
      try {
        const response = await getArticleComments(props.article_id);
        state.comments = response.results as unknown as Array<CommentInfo>;
      } catch (e) {
        console.error(e);
      }
    };

    const handleOk = async (): Promise<void> => {
      state.visible = false;
      await getCommentList();
    };

    // 添加评论
    const showCommentModal = (
      commentId: number,
      user: number,
      secondUser?: number
    ): boolean | void => {
      if (!window.sessionStorage.userInfo) {
        ElMessage({
          message: "登录才能点赞，请先登录！",
          type: "warning",
        });
        return false;
      }
      // 添加三级评论
      if (secondUser) {
        state.comment_id = commentId;
      } else {
        // 添加二级评论
        state.comment_id = commentId;
      }
      state.visible = true;
    };
    onMounted(() => {
      getCommentList();
    });

    return {
      state,
      showCommentModal,
      handleOk,
      handleCancel,
      formatTime,
    };
  },
});
</script>
<style lang="less" scoped>
.comment-list {
  text-align: center;
}

.comment-list {
  position: relative;
  text-align: left;
  padding-top: 30px;
  margin-top: 30px;
  border-top: 1px solid #eee;

  .avatar {
    position: absolute;
    left: 0px;
  }

  .el-icon-circle-plus {
    font-size: 40px;
  }
}

.clearfix {
  clear: both;
}

.comment-list {
  margin-top: 30px;

  .top-title {
    padding-bottom: 20px;
    font-size: 17px;
    font-weight: 700;
    border-bottom: 1px solid #f0f0f0;
  }

  .item {
    padding: 20px 0 30px;
    border-bottom: 1px solid #f0f0f0;

    .item-header {
      position: relative;
      padding-left: 45px;
      padding-bottom: 10px;

      .author {
        position: absolute;
        left: 0;
        display: inline-block;

        .avatar {
          display: inline-block;
          margin-right: 5px;
          width: 40px;
          height: 40px;
          vertical-align: middle;

          img {
            width: 100%;
            height: 100%;
            border-radius: 50%;
          }
        }
      }

      .info {
        display: inline-block;

        .name {
          font-size: 15px;
          color: #333;
        }

        .time {
          font-size: 12px;
          color: #969696;
        }
      }
    }

    .comment-detail {
      min-height: 40px;
    }

    .item-comment {
      .like {
        margin-right: 20px;
      }
    }
  }
}

.item-other {
  margin: 20px;
  padding: 10px;
  border-left: 2px solid #f0f0f0;

  .item-header {
    position: relative;
    padding-left: 45px;
    padding-bottom: 10px;

    .author {
      position: absolute;
      left: 0;
      display: inline-block;

      .avatar {
        display: inline-block;
        margin-right: 5px;
        width: 38px;
        height: 38px;
        vertical-align: middle;

        img {
          width: 100%;
          height: 100%;
          border-radius: 50%;
        }
      }
    }

    .info {
      display: inline-block;

      .name {
        font-size: 15px;
        color: #333;
      }

      .time {
        font-size: 12px;
        color: #969696;
      }
    }
  }

  .comment-detail {
    min-height: 40px;
    border-bottom: 1px dashed #f0f0f0;
  }

  .message {
    padding: 10px;
  }
}
</style>

