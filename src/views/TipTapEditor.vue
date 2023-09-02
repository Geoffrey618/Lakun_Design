<template>
  <div v-if="editor" style="margin-left: 20%;">
    <button @click="editor.chain().focus().toggleBold().run()" :disabled="!editor.can().chain().focus().toggleBold().run()" :class="{ 'is-active': editor.isActive('bold') }">
      bold
    </button>
    <button @click="editor.chain().focus().toggleItalic().run()" :disabled="!editor.can().chain().focus().toggleItalic().run()" :class="{ 'is-active': editor.isActive('italic') }">
      italic
    </button>
    <button @click="editor.chain().focus().toggleStrike().run()" :disabled="!editor.can().chain().focus().toggleStrike().run()" :class="{ 'is-active': editor.isActive('strike') }">
      strike
    </button>
    <button @click="editor.chain().focus().toggleCode().run()" :disabled="!editor.can().chain().focus().toggleCode().run()" :class="{ 'is-active': editor.isActive('code') }">
      code
    </button>
    <button @click="editor.chain().focus().unsetAllMarks().run()">
      clear marks
    </button>
    <button @click="editor.chain().focus().clearNodes().run()">
      clear nodes
    </button>
    <button @click="editor.chain().focus().setParagraph().run()" :class="{ 'is-active': editor.isActive('paragraph') }">
      paragraph
    </button>
    <button @click="editor.chain().focus().toggleHeading({ level: 1 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }">
      h1
    </button>
    <button @click="editor.chain().focus().toggleHeading({ level: 2 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }">
      h2
    </button>
    <button @click="editor.chain().focus().toggleHeading({ level: 3 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }">
      h3
    </button>
    <button @click="editor.chain().focus().toggleHeading({ level: 4 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 4 }) }">
      h4
    </button>
    <button @click="editor.chain().focus().toggleHeading({ level: 5 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 5 }) }">
      h5
    </button>
    <button @click="editor.chain().focus().toggleHeading({ level: 6 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 6 }) }">
      h6
    </button>
    <button @click="editor.chain().focus().toggleBulletList().run()" :class="{ 'is-active': editor.isActive('bulletList') }">
      bullet list
    </button>
    <button @click="editor.chain().focus().toggleOrderedList().run()" :class="{ 'is-active': editor.isActive('orderedList') }">
      ordered list
    </button>
    <button @click="editor.chain().focus().toggleCodeBlock().run()" :class="{ 'is-active': editor.isActive('codeBlock') }">
      code block
    </button>
    <button @click="editor.chain().focus().toggleBlockquote().run()" :class="{ 'is-active': editor.isActive('blockquote') }">
      blockquote
    </button>
    <button @click="editor.chain().focus().setHorizontalRule().run()">
      horizontal rule
    </button>
    <button @click="editor.chain().focus().setHardBreak().run()">
      hard break
    </button>
    <button @click="editor.chain().focus().undo().run()" :disabled="!editor.can().chain().focus().undo().run()">
      undo
    </button>
    <button @click="editor.chain().focus().redo().run()" :disabled="!editor.can().chain().focus().redo().run()">
      redo
    </button>
    <button @click="addImage">add image from URL</button>
    <button @click="addtable">add table</button>
    <button @click="editor.chain().focus().toggleHighlight().run()" :class="{ 'is-active': editor.isActive('highlight') }">
      highlight
    </button>
    <button @click="editor.chain().focus().setTextAlign('left').run()" :class="{ 'is-active': editor.isActive({ textAlign: 'left' }) }">
      left
    </button>
    <button @click="editor.chain().focus().setTextAlign('center').run()" :class="{ 'is-active': editor.isActive({ textAlign: 'center' }) }">
      center
    </button>
    <button @click="editor.chain().focus().setTextAlign('right').run()" :class="{ 'is-active': editor.isActive({ textAlign: 'right' }) }">
      right
    </button>
    <button @click="editor.chain().focus().setTextAlign('justify').run()" :class="{ 'is-active': editor.isActive({ textAlign: 'justify' }) }">
      justify
    </button>
    <button @click="draw">draw</button>
    <button id="add" @click="addVideo">
      Add YouTube video
    </button>
    <input
      id="width"
      type="number"
      v-model="width"
      placeholder="width"
      min="320"
      max="1024"
    >
    <input
      id="height"
      type="number"
      v-model="height"
      placeholder="height"
      min="180"
      max="720"
    >
    <br>
    <input
      type="color"
      @input="editor.chain().focus().setColor($event.target.value).run()"
      :value="editor.getAttributes('textStyle').color"
    >
    <button @click="editor.chain().focus().setColor('#958DF1').run()" :class="{ 'is-active': editor.isActive('textStyle', { color: '#958DF1' })}">
      purple
    </button>
    <button @click="editor.chain().focus().setColor('#F98181').run()" :class="{ 'is-active': editor.isActive('textStyle', { color: '#F98181' })}">
      red
    </button>
    <button @click="editor.chain().focus().setColor('#FBBC88').run()" :class="{ 'is-active': editor.isActive('textStyle', { color: '#FBBC88' })}">
      orange
    </button>
    <button @click="editor.chain().focus().setColor('#FAF594').run()" :class="{ 'is-active': editor.isActive('textStyle', { color: '#FAF594' })}">
      yellow
    </button>
    <button @click="editor.chain().focus().setColor('#70CFF8').run()" :class="{ 'is-active': editor.isActive('textStyle', { color: '#70CFF8' })}">
      blue
    </button>
    <button @click="editor.chain().focus().setColor('#94FADB').run()" :class="{ 'is-active': editor.isActive('textStyle', { color: '#94FADB' })}">
      teal
    </button>
    <button @click="editor.chain().focus().setColor('#B9F18D').run()" :class="{ 'is-active': editor.isActive('textStyle', { color: '#B9F18D' })}">
      green
    </button>
    <button @click="editor.chain().focus().unsetColor().run()">
      unsetColor
    </button>
    <el-select v-model="value" placeholder="请选择" @change="changetemplate">
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
    </el-select>
    <input v-model="userat">
    <button @click="atsomebody">@</button>
    <br>
    <input placeholder="请输入保存的文件名" v-model="this.tempFileName">
    <button @click="handleSaveToWord">save to word</button>
    <input v-model="this.document_title" placeholder="输入文档名">
    <input v-model="this.folderchosen" placeholder="保存位置">
    <button @click="createfile">创立文档</button>
    <input v-model="this.foldernamenow" placeholder="输入文件夹名">
    <button @click="createfolder">创立文件夹</button>
      <el-tree
        :data="datatree"
        show-checkbox
        node-key="id"
        default-expand-all
        :expand-on-click-node="false"
        :render-content="renderContent">
      </el-tree>
    <bubble-menu
      class="bubble-menu"
      :tippy-options="{ duration: 100 }"
      :editor="editor"
    >
      <button @click="editor.chain().focus().toggleBold().run()" :class="{ 'is-active': editor.isActive('bold') }">
        Bold
      </button>
      <button @click="editor.chain().focus().toggleItalic().run()" :class="{ 'is-active': editor.isActive('italic') }">
        Italic
      </button>
      <button @click="editor.chain().focus().toggleStrike().run()" :class="{ 'is-active': editor.isActive('strike') }">
        Strike
      </button>
      <button @click="createfile">创立文档</button>
    </bubble-menu>

    <floating-menu
      class="floating-menu"
      :tippy-options="{ duration: 100 }"
      :editor="editor"
    >
      <button @click="editor.chain().focus().toggleHeading({ level: 1 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }">
        H1
      </button>
      <button @click="editor.chain().focus().toggleHeading({ level: 2 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }">
        H2
      </button>
      <button @click="editor.chain().focus().toggleBulletList().run()" :class="{ 'is-active': editor.isActive('bulletList') }">
        Bullet List
      </button>
    </floating-menu>
    <div class="character-count" v-if="editor">
      {{ editor.storage.characterCount.characters() }}/{{ limit }} characters
      <br>
      {{ editor.storage.characterCount.words() }} words
    </div>
  </div>
  <editor-content :editor="editor"  style="margin-left: 20%;"/>
</template>

<script>
import htmlDocx from 'html-docx-js/dist/html-docx';
import {saveAs} from 'file-saver';
import VueHtml2pdf from "vue-html2pdf";
import { generateJSON } from '@tiptap/html'
import { generateHTML } from '@tiptap/html'
import Bold from '@tiptap/extension-bold'
import TextStyle from '@tiptap/extension-text-style'
import { Color } from '@tiptap/extension-color'
import CharacterCount from '@tiptap/extension-character-count'
import Youtube from '@tiptap/extension-youtube'
import Highlight from '@tiptap/extension-highlight'
import TextAlign from '@tiptap/extension-text-align'
import Document from '@tiptap/extension-document'
import Dropcursor from '@tiptap/extension-dropcursor'
import Image from '@tiptap/extension-image'
import Paragraph from '@tiptap/extension-paragraph'
import Text from '@tiptap/extension-text'
import StarterKit from '@tiptap/starter-kit'
import { Editor, EditorContent , BubbleMenu , FloatingMenu,} from '@tiptap/vue-3'
import axios from 'axios';

export default {
  components: {
    EditorContent,
    BubbleMenu,
    FloatingMenu,
  },

  data() {
    return {
      folderchosen:'',
      document_title:'',
      editor: null,
      width: '640',
      height: '480',
      limit: 5000,
      tempFileName:"file1",
      options: [{
          value: `temp1`,
          label: '模版1'
        }, {
          value: `temp2`,
          label: '模版2'
        }, {
          value: `temp3`,
          label: '模版3'
        }, {
          value: `temp4`,
          label: '模版4'
        }, {
          value: `temp5`,
          label: '模版5'
        }],
        value: '',
        datatree:[

        ],
        foldernamenow:''
    }
  },
  methods:{
    addImage(){
      const url = window.prompt('URL')

      if (url) {
        this.editor.chain().focus().setImage({ src: url }).run()
      }
    },
    addtable(){
      this.$router.replace('/editortable')
    },
    draw(){
      this.$router.replace('./draw')
    },
    addVideo() {
      const url = prompt('Enter YouTube URL')

      this.editor.commands.setYoutubeVideo({
        src: url,
        width: Math.max(320, parseInt(this.width, 10)) || 640,
        height: Math.max(180, parseInt(this.height, 10)) || 480,
      })
    },
    ContentSet(){
      this.editor.commands.setContent("`"+this.html+"`")
    },
    handleSaveToWord() {
    // this.content 富文本内容
    // this.tempFileName 导出的文件名
    console.log("'"+this.editor.getHTML()+"'")
    var converted = htmlDocx.asBlob("'"+this.editor.getHTML()+"'");
    saveAs(converted, this.tempFileName);
  },
    changetemplate(){
      this.editor.commands.setContent(this.value)
    },
    createfile(){
      console.log(JSON.stringify(typeof(this.editor.getJSON())))
      for(var i=0;i<this.datatree.length;i++){
        if(this.datatree[i].foldername==this.folderchosen){
          this.datatree[i].children.push({
            foldername:this.document_title,
            children:[],
            label:this.document_title
          })
        }
      }
      axios({
        method:'post',
        url:'http://8.130.38.119:12000/documents/create_document/',
        data:{
          document_title:this.document_title,
          document_content:JSON.stringify(typeof(this.editor.getJSON())),
          project_id:27,
          foldername:this.document_title
        }
      })
    },
    createfolder(){
      this.datatree.push({
        foldername:this.foldernamenow,
        children:[],
        label:this.foldernamenow,
      })
      axios({
        method:'post',
        url:'http://8.130.38.119:12000/documents/create_folder/',
        data:{
          //documenttitle:this.document_title,
          //documentcontent:JSON.stringify(typeof(this.editor.getJSON())),
          project_id:27,
          foldername:this.foldernamenow
          
        }
      })

    },
    atsomebody(){
      axios({
        method:'post',
        url:'http://8.130.38.119:12000/documents/receive_message/',
        data:{
          documenttitle:'',
          documentcontent:this.userat,
          //username:this.$store.state.username
          username:this.$store.state.username_glo,
        }
      })
    }


  },
  created(){
    axios({
        method:'post',
        url:'http://8.130.38.119:12000/documents/document_detail/',
        data:{
          documentid:2,
        }
        
      }).then((res)=>{
        //console.log(res)
        this.editor.commands.setContent(JSON.parse(res.data.documentcontent))
      })

      axios({
        method:'post',
        url:'http://8.130.38.119:12000/documents/get_dic/',
        data:{
          project_id:27,
        }
        
      }).then((res)=>{
        //console.log(res)
        //this.editor.commands.setContent(JSON.parse(res.data.documentcontent))
        //console.log(res.data)
        //console.log(res.data)
        //this.datatree=res.data
        //console.log(res.data)
        //console.log(typeof(this.datatree))
        //console.log(res.data.result)
        for(var i=0;i<res.data.result.length;i++){
          this.datatree.push(res.data.result[i])
        }
        //console.log(this.datatree)
      })

  },

  mounted() {
    this.editor = new Editor({
      autofocus: 'start',
      editable: true,
      extensions: [
        StarterKit,
        Document,
        Paragraph,
        Text,
        Image,
        Dropcursor,
        TextStyle,
        Color,
        TextAlign.configure({
          types: ['heading', 'paragraph'],
        }),
        Highlight,
        Youtube.configure({
          controls: false,
        }),
        CharacterCount.configure({
          limit: this.limit,
        }),
      ],
      content: `
        <h2>
          Hi there,
        </h2>
        <p>
          this is a <em>basic</em> example of <strong>tiptap</strong>. Sure, there are all kind of basic text styles you’d probably expect from a text editor. But wait until you see the lists:
        </p>
        <ul>
          <li>
            That’s a bullet list with one …
          </li>
          <li>
            … or two list items.
          </li>
        </ul>
        <p>
          Isn’t that great? And all of that is editable. But wait, there’s more. Let’s try a code block:
        </p>
        <pre><code class="language-css">body {
  display: none;
}</code></pre>
        <p>
          I know, I know, this is impressive. It’s only the tip of the iceberg though. Give it a try and click a little bit around. Don’t forget to check the other examples too.
        </p>
        <blockquote>
          Wow, that’s amazing. Good work, boy! 👏
          <br />
          — Mom
        </blockquote>
      `,
      onUpdate: ({ editor }) => {
      const json = editor.getJSON()
      const html = editor.getHTML()
    // send the content to an API here
    },
      editorProps: {
        attributes: {
          spellcheck: 'false',
        },
      },
    })
  },

  beforeUnmount() {
    this.editor.destroy()
  },
  computed:{
    output1() {
      return generateHTML(json, [
        Document,
        Paragraph,
        Text,
        Bold,
        // other extensions …
      ])
    },
    output2() {
      return generateJSON(html, [
        Document,
        Paragraph,
        Text,
        Bold,
        // other extensions …
      ])
    },
  }
}
</script>

<style lang="scss">
/* Basic editor styles */
.character-count {
  margin-top: 1rem;
  color: #868e96;
}
.tiptap {
  > * + * {
    margin-top: 0.75em;
  }

  ul,
  ol {
    padding: 0 1rem;
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    line-height: 1.1;
  }

  code {
    background-color: rgba(#616161, 0.1);
    color: #616161;
  }

  pre {
    background: #0D0D0D;
    color: #FFF;
    font-family: 'JetBrainsMono', monospace;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;

    code {
      color: inherit;
      padding: 0;
      background: none;
      font-size: 0.8rem;
    }
  }

  img {
    max-width: 100%;
    height: auto;
  }

  blockquote {
    padding-left: 1rem;
    border-left: 2px solid rgba(#0D0D0D, 0.1);
  }

  hr {
    border: none;
    border-top: 2px solid rgba(#0D0D0D, 0.1);
    margin: 2rem 0;
  }
}
</style>