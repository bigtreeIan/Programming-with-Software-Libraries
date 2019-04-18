<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US">
<head>
<link rel="icon" href="/cpython/static/hgicon.png" type="image/png" />
<meta name="robots" content="index, nofollow" />
<link rel="stylesheet" href="/cpython/static/style-paper.css" type="text/css" />
<script type="text/javascript" src="/cpython/static/mercurial.js"></script>

<link rel="stylesheet" href="/cpython/highlightcss" type="text/css" />
<title>cpython: 283036fe48e2 Lib/shutil.py</title>
</head>
<body>

<div class="container">
<div class="menu">
<div class="logo">
<a href="https://hg.python.org">
<img src="/cpython/static/hglogo.png" alt="back to hg.python.org repositories" /></a>
</div>
<ul>
<li><a href="/cpython/shortlog/283036fe48e2">log</a></li>
<li><a href="/cpython/graph/283036fe48e2">graph</a></li>
<li><a href="/cpython/tags">tags</a></li>
<li><a href="/cpython/branches">branches</a></li>
</ul>
<ul>
<li><a href="/cpython/rev/283036fe48e2">changeset</a></li>
<li><a href="/cpython/file/283036fe48e2/Lib/">browse</a></li>
</ul>
<ul>
<li class="active">file</li>
<li><a href="/cpython/file/tip/Lib/shutil.py">latest</a></li>
<li><a href="/cpython/diff/283036fe48e2/Lib/shutil.py">diff</a></li>
<li><a href="/cpython/comparison/283036fe48e2/Lib/shutil.py">comparison</a></li>
<li><a href="/cpython/annotate/283036fe48e2/Lib/shutil.py">annotate</a></li>
<li><a href="/cpython/log/283036fe48e2/Lib/shutil.py">file log</a></li>
<li><a href="/cpython/raw-file/283036fe48e2/Lib/shutil.py">raw</a></li>
</ul>
<ul>
<li><a href="/cpython/help">help</a></li>
</ul>
</div>

<div class="main">
<h2 class="breadcrumb"><a href="/">Mercurial</a> &gt; <a href="/cpython">cpython</a> </h2>
<h3>view Lib/shutil.py @ 95492:283036fe48e2</h3>

<form class="search" action="/cpython/log">

<p><input name="rev" id="search1" type="text" size="30" /></p>
<div id="hint">Find changesets by keywords (author, files, the commit message), revision
number or hash, or <a href="/cpython/help/revsets">revset expression</a>.</div>
</form>

<div class="description">Fix typo in telnet docs (reported by Keith Briggs)</div>

<table id="changesetEntry">
<tr>
 <th class="author">author</th>
 <td class="author">&#84;&#105;&#109;&#32;&#71;&#111;&#108;&#100;&#101;&#110;&#32;&#60;&#109;&#97;&#105;&#108;&#64;&#116;&#105;&#109;&#103;&#111;&#108;&#100;&#101;&#110;&#46;&#109;&#101;&#46;&#117;&#107;&#62;</td>
</tr>
<tr>
 <th class="date">date</th>
 <td class="date age">Wed, 08 Apr 2015 16:52:27 +0100</td>
</tr>
<tr>
 <th class="author">parents</th>
 <td class="author"><a href="/cpython/file/8fa9097eadcb/Lib/shutil.py">8fa9097eadcb</a> </td>
</tr>
<tr>
 <th class="author">children</th>
 <td class="author"><a href="/cpython/file/7d5754af95a9/Lib/shutil.py">7d5754af95a9</a> </td>
</tr>
</table>

<div class="overflow">
<div class="sourcefirst linewraptoggle">line wrap: <a class="linewraplink" href="javascript:toggleLinewrap()">on</a></div>
<div class="sourcefirst"> line source</div>
<pre class="sourcelines stripes4 wrap">
<span id="l1"><span class="sd">&quot;&quot;&quot;Utility functions for copying and archiving files and directory trees.</span></span><a href="#l1"></a>
<span id="l2"></span><a href="#l2"></a>
<span id="l3"><span class="sd">XXX The functions here don&#39;t copy the resource fork or other metadata on Mac.</span></span><a href="#l3"></a>
<span id="l4"></span><a href="#l4"></a>
<span id="l5"><span class="sd">&quot;&quot;&quot;</span></span><a href="#l5"></a>
<span id="l6"></span><a href="#l6"></a>
<span id="l7"><span class="kn">import</span> <span class="nn">os</span></span><a href="#l7"></a>
<span id="l8"><span class="kn">import</span> <span class="nn">sys</span></span><a href="#l8"></a>
<span id="l9"><span class="kn">import</span> <span class="nn">stat</span></span><a href="#l9"></a>
<span id="l10"><span class="kn">from</span> <span class="nn">os.path</span> <span class="kn">import</span> <span class="n">abspath</span></span><a href="#l10"></a>
<span id="l11"><span class="kn">import</span> <span class="nn">fnmatch</span></span><a href="#l11"></a>
<span id="l12"><span class="kn">import</span> <span class="nn">collections</span></span><a href="#l12"></a>
<span id="l13"><span class="kn">import</span> <span class="nn">errno</span></span><a href="#l13"></a>
<span id="l14"><span class="kn">import</span> <span class="nn">tarfile</span></span><a href="#l14"></a>
<span id="l15"></span><a href="#l15"></a>
<span id="l16"><span class="k">try</span><span class="p">:</span></span><a href="#l16"></a>
<span id="l17">    <span class="kn">import</span> <span class="nn">bz2</span></span><a href="#l17"></a>
<span id="l18">    <span class="k">del</span> <span class="n">bz2</span></span><a href="#l18"></a>
<span id="l19">    <span class="n">_BZ2_SUPPORTED</span> <span class="o">=</span> <span class="bp">True</span></span><a href="#l19"></a>
<span id="l20"><span class="k">except</span> <span class="ne">ImportError</span><span class="p">:</span></span><a href="#l20"></a>
<span id="l21">    <span class="n">_BZ2_SUPPORTED</span> <span class="o">=</span> <span class="bp">False</span></span><a href="#l21"></a>
<span id="l22"></span><a href="#l22"></a>
<span id="l23"><span class="k">try</span><span class="p">:</span></span><a href="#l23"></a>
<span id="l24">    <span class="kn">from</span> <span class="nn">pwd</span> <span class="kn">import</span> <span class="n">getpwnam</span></span><a href="#l24"></a>
<span id="l25"><span class="k">except</span> <span class="ne">ImportError</span><span class="p">:</span></span><a href="#l25"></a>
<span id="l26">    <span class="n">getpwnam</span> <span class="o">=</span> <span class="bp">None</span></span><a href="#l26"></a>
<span id="l27"></span><a href="#l27"></a>
<span id="l28"><span class="k">try</span><span class="p">:</span></span><a href="#l28"></a>
<span id="l29">    <span class="kn">from</span> <span class="nn">grp</span> <span class="kn">import</span> <span class="n">getgrnam</span></span><a href="#l29"></a>
<span id="l30"><span class="k">except</span> <span class="ne">ImportError</span><span class="p">:</span></span><a href="#l30"></a>
<span id="l31">    <span class="n">getgrnam</span> <span class="o">=</span> <span class="bp">None</span></span><a href="#l31"></a>
<span id="l32"></span><a href="#l32"></a>
<span id="l33"><span class="n">__all__</span> <span class="o">=</span> <span class="p">[</span><span class="s">&quot;copyfileobj&quot;</span><span class="p">,</span> <span class="s">&quot;copyfile&quot;</span><span class="p">,</span> <span class="s">&quot;copymode&quot;</span><span class="p">,</span> <span class="s">&quot;copystat&quot;</span><span class="p">,</span> <span class="s">&quot;copy&quot;</span><span class="p">,</span> <span class="s">&quot;copy2&quot;</span><span class="p">,</span></span><a href="#l33"></a>
<span id="l34">           <span class="s">&quot;copytree&quot;</span><span class="p">,</span> <span class="s">&quot;move&quot;</span><span class="p">,</span> <span class="s">&quot;rmtree&quot;</span><span class="p">,</span> <span class="s">&quot;Error&quot;</span><span class="p">,</span> <span class="s">&quot;SpecialFileError&quot;</span><span class="p">,</span></span><a href="#l34"></a>
<span id="l35">           <span class="s">&quot;ExecError&quot;</span><span class="p">,</span> <span class="s">&quot;make_archive&quot;</span><span class="p">,</span> <span class="s">&quot;get_archive_formats&quot;</span><span class="p">,</span></span><a href="#l35"></a>
<span id="l36">           <span class="s">&quot;register_archive_format&quot;</span><span class="p">,</span> <span class="s">&quot;unregister_archive_format&quot;</span><span class="p">,</span></span><a href="#l36"></a>
<span id="l37">           <span class="s">&quot;get_unpack_formats&quot;</span><span class="p">,</span> <span class="s">&quot;register_unpack_format&quot;</span><span class="p">,</span></span><a href="#l37"></a>
<span id="l38">           <span class="s">&quot;unregister_unpack_format&quot;</span><span class="p">,</span> <span class="s">&quot;unpack_archive&quot;</span><span class="p">,</span></span><a href="#l38"></a>
<span id="l39">           <span class="s">&quot;ignore_patterns&quot;</span><span class="p">,</span> <span class="s">&quot;chown&quot;</span><span class="p">,</span> <span class="s">&quot;which&quot;</span><span class="p">,</span> <span class="s">&quot;get_terminal_size&quot;</span><span class="p">,</span></span><a href="#l39"></a>
<span id="l40">           <span class="s">&quot;SameFileError&quot;</span><span class="p">]</span></span><a href="#l40"></a>
<span id="l41">           <span class="c"># disk_usage is added later, if available on the platform</span></span><a href="#l41"></a>
<span id="l42"></span><a href="#l42"></a>
<span id="l43"><span class="k">class</span> <span class="nc">Error</span><span class="p">(</span><span class="ne">OSError</span><span class="p">):</span></span><a href="#l43"></a>
<span id="l44">    <span class="k">pass</span></span><a href="#l44"></a>
<span id="l45"></span><a href="#l45"></a>
<span id="l46"><span class="k">class</span> <span class="nc">SameFileError</span><span class="p">(</span><span class="n">Error</span><span class="p">):</span></span><a href="#l46"></a>
<span id="l47">    <span class="sd">&quot;&quot;&quot;Raised when source and destination are the same file.&quot;&quot;&quot;</span></span><a href="#l47"></a>
<span id="l48"></span><a href="#l48"></a>
<span id="l49"><span class="k">class</span> <span class="nc">SpecialFileError</span><span class="p">(</span><span class="ne">OSError</span><span class="p">):</span></span><a href="#l49"></a>
<span id="l50">    <span class="sd">&quot;&quot;&quot;Raised when trying to do a kind of operation (e.g. copying) which is</span></span><a href="#l50"></a>
<span id="l51"><span class="sd">    not supported on a special file (e.g. a named pipe)&quot;&quot;&quot;</span></span><a href="#l51"></a>
<span id="l52"></span><a href="#l52"></a>
<span id="l53"><span class="k">class</span> <span class="nc">ExecError</span><span class="p">(</span><span class="ne">OSError</span><span class="p">):</span></span><a href="#l53"></a>
<span id="l54">    <span class="sd">&quot;&quot;&quot;Raised when a command could not be executed&quot;&quot;&quot;</span></span><a href="#l54"></a>
<span id="l55"></span><a href="#l55"></a>
<span id="l56"><span class="k">class</span> <span class="nc">ReadError</span><span class="p">(</span><span class="ne">OSError</span><span class="p">):</span></span><a href="#l56"></a>
<span id="l57">    <span class="sd">&quot;&quot;&quot;Raised when an archive cannot be read&quot;&quot;&quot;</span></span><a href="#l57"></a>
<span id="l58"></span><a href="#l58"></a>
<span id="l59"><span class="k">class</span> <span class="nc">RegistryError</span><span class="p">(</span><span class="ne">Exception</span><span class="p">):</span></span><a href="#l59"></a>
<span id="l60">    <span class="sd">&quot;&quot;&quot;Raised when a registry operation with the archiving</span></span><a href="#l60"></a>
<span id="l61"><span class="sd">    and unpacking registeries fails&quot;&quot;&quot;</span></span><a href="#l61"></a>
<span id="l62"></span><a href="#l62"></a>
<span id="l63"></span><a href="#l63"></a>
<span id="l64"><span class="k">def</span> <span class="nf">copyfileobj</span><span class="p">(</span><span class="n">fsrc</span><span class="p">,</span> <span class="n">fdst</span><span class="p">,</span> <span class="n">length</span><span class="o">=</span><span class="mi">16</span><span class="o">*</span><span class="mi">1024</span><span class="p">):</span></span><a href="#l64"></a>
<span id="l65">    <span class="sd">&quot;&quot;&quot;copy data from file-like object fsrc to file-like object fdst&quot;&quot;&quot;</span></span><a href="#l65"></a>
<span id="l66">    <span class="k">while</span> <span class="mi">1</span><span class="p">:</span></span><a href="#l66"></a>
<span id="l67">        <span class="n">buf</span> <span class="o">=</span> <span class="n">fsrc</span><span class="o">.</span><span class="n">read</span><span class="p">(</span><span class="n">length</span><span class="p">)</span></span><a href="#l67"></a>
<span id="l68">        <span class="k">if</span> <span class="ow">not</span> <span class="n">buf</span><span class="p">:</span></span><a href="#l68"></a>
<span id="l69">            <span class="k">break</span></span><a href="#l69"></a>
<span id="l70">        <span class="n">fdst</span><span class="o">.</span><span class="n">write</span><span class="p">(</span><span class="n">buf</span><span class="p">)</span></span><a href="#l70"></a>
<span id="l71"></span><a href="#l71"></a>
<span id="l72"><span class="k">def</span> <span class="nf">_samefile</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">):</span></span><a href="#l72"></a>
<span id="l73">    <span class="c"># Macintosh, Unix.</span></span><a href="#l73"></a>
<span id="l74">    <span class="k">if</span> <span class="nb">hasattr</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="p">,</span> <span class="s">&#39;samefile&#39;</span><span class="p">):</span></span><a href="#l74"></a>
<span id="l75">        <span class="k">try</span><span class="p">:</span></span><a href="#l75"></a>
<span id="l76">            <span class="k">return</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">samefile</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">)</span></span><a href="#l76"></a>
<span id="l77">        <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l77"></a>
<span id="l78">            <span class="k">return</span> <span class="bp">False</span></span><a href="#l78"></a>
<span id="l79"></span><a href="#l79"></a>
<span id="l80">    <span class="c"># All other platforms: check for same pathname.</span></span><a href="#l80"></a>
<span id="l81">    <span class="k">return</span> <span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">normcase</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">abspath</span><span class="p">(</span><span class="n">src</span><span class="p">))</span> <span class="o">==</span></span><a href="#l81"></a>
<span id="l82">            <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">normcase</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">abspath</span><span class="p">(</span><span class="n">dst</span><span class="p">)))</span></span><a href="#l82"></a>
<span id="l83"></span><a href="#l83"></a>
<span id="l84"><span class="k">def</span> <span class="nf">copyfile</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">,</span> <span class="o">*</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="bp">True</span><span class="p">):</span></span><a href="#l84"></a>
<span id="l85">    <span class="sd">&quot;&quot;&quot;Copy data from src to dst.</span></span><a href="#l85"></a>
<span id="l86"></span><a href="#l86"></a>
<span id="l87"><span class="sd">    If follow_symlinks is not set and src is a symbolic link, a new</span></span><a href="#l87"></a>
<span id="l88"><span class="sd">    symlink will be created instead of copying the file it points to.</span></span><a href="#l88"></a>
<span id="l89"></span><a href="#l89"></a>
<span id="l90"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l90"></a>
<span id="l91">    <span class="k">if</span> <span class="n">_samefile</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">):</span></span><a href="#l91"></a>
<span id="l92">        <span class="k">raise</span> <span class="n">SameFileError</span><span class="p">(</span><span class="s">&quot;{!r} and {!r} are the same file&quot;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">))</span></span><a href="#l92"></a>
<span id="l93"></span><a href="#l93"></a>
<span id="l94">    <span class="k">for</span> <span class="n">fn</span> <span class="ow">in</span> <span class="p">[</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">]:</span></span><a href="#l94"></a>
<span id="l95">        <span class="k">try</span><span class="p">:</span></span><a href="#l95"></a>
<span id="l96">            <span class="n">st</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">stat</span><span class="p">(</span><span class="n">fn</span><span class="p">)</span></span><a href="#l96"></a>
<span id="l97">        <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l97"></a>
<span id="l98">            <span class="c"># File most likely does not exist</span></span><a href="#l98"></a>
<span id="l99">            <span class="k">pass</span></span><a href="#l99"></a>
<span id="l100">        <span class="k">else</span><span class="p">:</span></span><a href="#l100"></a>
<span id="l101">            <span class="c"># XXX What about other special files? (sockets, devices...)</span></span><a href="#l101"></a>
<span id="l102">            <span class="k">if</span> <span class="n">stat</span><span class="o">.</span><span class="n">S_ISFIFO</span><span class="p">(</span><span class="n">st</span><span class="o">.</span><span class="n">st_mode</span><span class="p">):</span></span><a href="#l102"></a>
<span id="l103">                <span class="k">raise</span> <span class="n">SpecialFileError</span><span class="p">(</span><span class="s">&quot;`</span><span class="si">%s</span><span class="s">` is a named pipe&quot;</span> <span class="o">%</span> <span class="n">fn</span><span class="p">)</span></span><a href="#l103"></a>
<span id="l104"></span><a href="#l104"></a>
<span id="l105">    <span class="k">if</span> <span class="ow">not</span> <span class="n">follow_symlinks</span> <span class="ow">and</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">islink</span><span class="p">(</span><span class="n">src</span><span class="p">):</span></span><a href="#l105"></a>
<span id="l106">        <span class="n">os</span><span class="o">.</span><span class="n">symlink</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">readlink</span><span class="p">(</span><span class="n">src</span><span class="p">),</span> <span class="n">dst</span><span class="p">)</span></span><a href="#l106"></a>
<span id="l107">    <span class="k">else</span><span class="p">:</span></span><a href="#l107"></a>
<span id="l108">        <span class="k">with</span> <span class="nb">open</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="s">&#39;rb&#39;</span><span class="p">)</span> <span class="k">as</span> <span class="n">fsrc</span><span class="p">:</span></span><a href="#l108"></a>
<span id="l109">            <span class="k">with</span> <span class="nb">open</span><span class="p">(</span><span class="n">dst</span><span class="p">,</span> <span class="s">&#39;wb&#39;</span><span class="p">)</span> <span class="k">as</span> <span class="n">fdst</span><span class="p">:</span></span><a href="#l109"></a>
<span id="l110">                <span class="n">copyfileobj</span><span class="p">(</span><span class="n">fsrc</span><span class="p">,</span> <span class="n">fdst</span><span class="p">)</span></span><a href="#l110"></a>
<span id="l111">    <span class="k">return</span> <span class="n">dst</span></span><a href="#l111"></a>
<span id="l112"></span><a href="#l112"></a>
<span id="l113"><span class="k">def</span> <span class="nf">copymode</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">,</span> <span class="o">*</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="bp">True</span><span class="p">):</span></span><a href="#l113"></a>
<span id="l114">    <span class="sd">&quot;&quot;&quot;Copy mode bits from src to dst.</span></span><a href="#l114"></a>
<span id="l115"></span><a href="#l115"></a>
<span id="l116"><span class="sd">    If follow_symlinks is not set, symlinks aren&#39;t followed if and only</span></span><a href="#l116"></a>
<span id="l117"><span class="sd">    if both `src` and `dst` are symlinks.  If `lchmod` isn&#39;t available</span></span><a href="#l117"></a>
<span id="l118"><span class="sd">    (e.g. Linux) this method does nothing.</span></span><a href="#l118"></a>
<span id="l119"></span><a href="#l119"></a>
<span id="l120"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l120"></a>
<span id="l121">    <span class="k">if</span> <span class="ow">not</span> <span class="n">follow_symlinks</span> <span class="ow">and</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">islink</span><span class="p">(</span><span class="n">src</span><span class="p">)</span> <span class="ow">and</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">islink</span><span class="p">(</span><span class="n">dst</span><span class="p">):</span></span><a href="#l121"></a>
<span id="l122">        <span class="k">if</span> <span class="nb">hasattr</span><span class="p">(</span><span class="n">os</span><span class="p">,</span> <span class="s">&#39;lchmod&#39;</span><span class="p">):</span></span><a href="#l122"></a>
<span id="l123">            <span class="n">stat_func</span><span class="p">,</span> <span class="n">chmod_func</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">lstat</span><span class="p">,</span> <span class="n">os</span><span class="o">.</span><span class="n">lchmod</span></span><a href="#l123"></a>
<span id="l124">        <span class="k">else</span><span class="p">:</span></span><a href="#l124"></a>
<span id="l125">            <span class="k">return</span></span><a href="#l125"></a>
<span id="l126">    <span class="k">elif</span> <span class="nb">hasattr</span><span class="p">(</span><span class="n">os</span><span class="p">,</span> <span class="s">&#39;chmod&#39;</span><span class="p">):</span></span><a href="#l126"></a>
<span id="l127">        <span class="n">stat_func</span><span class="p">,</span> <span class="n">chmod_func</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">stat</span><span class="p">,</span> <span class="n">os</span><span class="o">.</span><span class="n">chmod</span></span><a href="#l127"></a>
<span id="l128">    <span class="k">else</span><span class="p">:</span></span><a href="#l128"></a>
<span id="l129">        <span class="k">return</span></span><a href="#l129"></a>
<span id="l130"></span><a href="#l130"></a>
<span id="l131">    <span class="n">st</span> <span class="o">=</span> <span class="n">stat_func</span><span class="p">(</span><span class="n">src</span><span class="p">)</span></span><a href="#l131"></a>
<span id="l132">    <span class="n">chmod_func</span><span class="p">(</span><span class="n">dst</span><span class="p">,</span> <span class="n">stat</span><span class="o">.</span><span class="n">S_IMODE</span><span class="p">(</span><span class="n">st</span><span class="o">.</span><span class="n">st_mode</span><span class="p">))</span></span><a href="#l132"></a>
<span id="l133"></span><a href="#l133"></a>
<span id="l134"><span class="k">if</span> <span class="nb">hasattr</span><span class="p">(</span><span class="n">os</span><span class="p">,</span> <span class="s">&#39;listxattr&#39;</span><span class="p">):</span></span><a href="#l134"></a>
<span id="l135">    <span class="k">def</span> <span class="nf">_copyxattr</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">,</span> <span class="o">*</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="bp">True</span><span class="p">):</span></span><a href="#l135"></a>
<span id="l136">        <span class="sd">&quot;&quot;&quot;Copy extended filesystem attributes from `src` to `dst`.</span></span><a href="#l136"></a>
<span id="l137"></span><a href="#l137"></a>
<span id="l138"><span class="sd">        Overwrite existing attributes.</span></span><a href="#l138"></a>
<span id="l139"></span><a href="#l139"></a>
<span id="l140"><span class="sd">        If `follow_symlinks` is false, symlinks won&#39;t be followed.</span></span><a href="#l140"></a>
<span id="l141"></span><a href="#l141"></a>
<span id="l142"><span class="sd">        &quot;&quot;&quot;</span></span><a href="#l142"></a>
<span id="l143"></span><a href="#l143"></a>
<span id="l144">        <span class="k">try</span><span class="p">:</span></span><a href="#l144"></a>
<span id="l145">            <span class="n">names</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">listxattr</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="n">follow_symlinks</span><span class="p">)</span></span><a href="#l145"></a>
<span id="l146">        <span class="k">except</span> <span class="ne">OSError</span> <span class="k">as</span> <span class="n">e</span><span class="p">:</span></span><a href="#l146"></a>
<span id="l147">            <span class="k">if</span> <span class="n">e</span><span class="o">.</span><span class="n">errno</span> <span class="ow">not</span> <span class="ow">in</span> <span class="p">(</span><span class="n">errno</span><span class="o">.</span><span class="n">ENOTSUP</span><span class="p">,</span> <span class="n">errno</span><span class="o">.</span><span class="n">ENODATA</span><span class="p">):</span></span><a href="#l147"></a>
<span id="l148">                <span class="k">raise</span></span><a href="#l148"></a>
<span id="l149">            <span class="k">return</span></span><a href="#l149"></a>
<span id="l150">        <span class="k">for</span> <span class="n">name</span> <span class="ow">in</span> <span class="n">names</span><span class="p">:</span></span><a href="#l150"></a>
<span id="l151">            <span class="k">try</span><span class="p">:</span></span><a href="#l151"></a>
<span id="l152">                <span class="n">value</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getxattr</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="n">follow_symlinks</span><span class="p">)</span></span><a href="#l152"></a>
<span id="l153">                <span class="n">os</span><span class="o">.</span><span class="n">setxattr</span><span class="p">(</span><span class="n">dst</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="n">value</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="n">follow_symlinks</span><span class="p">)</span></span><a href="#l153"></a>
<span id="l154">            <span class="k">except</span> <span class="ne">OSError</span> <span class="k">as</span> <span class="n">e</span><span class="p">:</span></span><a href="#l154"></a>
<span id="l155">                <span class="k">if</span> <span class="n">e</span><span class="o">.</span><span class="n">errno</span> <span class="ow">not</span> <span class="ow">in</span> <span class="p">(</span><span class="n">errno</span><span class="o">.</span><span class="n">EPERM</span><span class="p">,</span> <span class="n">errno</span><span class="o">.</span><span class="n">ENOTSUP</span><span class="p">,</span> <span class="n">errno</span><span class="o">.</span><span class="n">ENODATA</span><span class="p">):</span></span><a href="#l155"></a>
<span id="l156">                    <span class="k">raise</span></span><a href="#l156"></a>
<span id="l157"><span class="k">else</span><span class="p">:</span></span><a href="#l157"></a>
<span id="l158">    <span class="k">def</span> <span class="nf">_copyxattr</span><span class="p">(</span><span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span></span><a href="#l158"></a>
<span id="l159">        <span class="k">pass</span></span><a href="#l159"></a>
<span id="l160"></span><a href="#l160"></a>
<span id="l161"><span class="k">def</span> <span class="nf">copystat</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">,</span> <span class="o">*</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="bp">True</span><span class="p">):</span></span><a href="#l161"></a>
<span id="l162">    <span class="sd">&quot;&quot;&quot;Copy all stat info (mode bits, atime, mtime, flags) from src to dst.</span></span><a href="#l162"></a>
<span id="l163"></span><a href="#l163"></a>
<span id="l164"><span class="sd">    If the optional flag `follow_symlinks` is not set, symlinks aren&#39;t followed if and</span></span><a href="#l164"></a>
<span id="l165"><span class="sd">    only if both `src` and `dst` are symlinks.</span></span><a href="#l165"></a>
<span id="l166"></span><a href="#l166"></a>
<span id="l167"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l167"></a>
<span id="l168">    <span class="k">def</span> <span class="nf">_nop</span><span class="p">(</span><span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="n">ns</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="bp">None</span><span class="p">):</span></span><a href="#l168"></a>
<span id="l169">        <span class="k">pass</span></span><a href="#l169"></a>
<span id="l170"></span><a href="#l170"></a>
<span id="l171">    <span class="c"># follow symlinks (aka don&#39;t not follow symlinks)</span></span><a href="#l171"></a>
<span id="l172">    <span class="n">follow</span> <span class="o">=</span> <span class="n">follow_symlinks</span> <span class="ow">or</span> <span class="ow">not</span> <span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">islink</span><span class="p">(</span><span class="n">src</span><span class="p">)</span> <span class="ow">and</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">islink</span><span class="p">(</span><span class="n">dst</span><span class="p">))</span></span><a href="#l172"></a>
<span id="l173">    <span class="k">if</span> <span class="n">follow</span><span class="p">:</span></span><a href="#l173"></a>
<span id="l174">        <span class="c"># use the real function if it exists</span></span><a href="#l174"></a>
<span id="l175">        <span class="k">def</span> <span class="nf">lookup</span><span class="p">(</span><span class="n">name</span><span class="p">):</span></span><a href="#l175"></a>
<span id="l176">            <span class="k">return</span> <span class="nb">getattr</span><span class="p">(</span><span class="n">os</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="n">_nop</span><span class="p">)</span></span><a href="#l176"></a>
<span id="l177">    <span class="k">else</span><span class="p">:</span></span><a href="#l177"></a>
<span id="l178">        <span class="c"># use the real function only if it exists</span></span><a href="#l178"></a>
<span id="l179">        <span class="c"># *and* it supports follow_symlinks</span></span><a href="#l179"></a>
<span id="l180">        <span class="k">def</span> <span class="nf">lookup</span><span class="p">(</span><span class="n">name</span><span class="p">):</span></span><a href="#l180"></a>
<span id="l181">            <span class="n">fn</span> <span class="o">=</span> <span class="nb">getattr</span><span class="p">(</span><span class="n">os</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="n">_nop</span><span class="p">)</span></span><a href="#l181"></a>
<span id="l182">            <span class="k">if</span> <span class="n">fn</span> <span class="ow">in</span> <span class="n">os</span><span class="o">.</span><span class="n">supports_follow_symlinks</span><span class="p">:</span></span><a href="#l182"></a>
<span id="l183">                <span class="k">return</span> <span class="n">fn</span></span><a href="#l183"></a>
<span id="l184">            <span class="k">return</span> <span class="n">_nop</span></span><a href="#l184"></a>
<span id="l185"></span><a href="#l185"></a>
<span id="l186">    <span class="n">st</span> <span class="o">=</span> <span class="n">lookup</span><span class="p">(</span><span class="s">&quot;stat&quot;</span><span class="p">)(</span><span class="n">src</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="n">follow</span><span class="p">)</span></span><a href="#l186"></a>
<span id="l187">    <span class="n">mode</span> <span class="o">=</span> <span class="n">stat</span><span class="o">.</span><span class="n">S_IMODE</span><span class="p">(</span><span class="n">st</span><span class="o">.</span><span class="n">st_mode</span><span class="p">)</span></span><a href="#l187"></a>
<span id="l188">    <span class="n">lookup</span><span class="p">(</span><span class="s">&quot;utime&quot;</span><span class="p">)(</span><span class="n">dst</span><span class="p">,</span> <span class="n">ns</span><span class="o">=</span><span class="p">(</span><span class="n">st</span><span class="o">.</span><span class="n">st_atime_ns</span><span class="p">,</span> <span class="n">st</span><span class="o">.</span><span class="n">st_mtime_ns</span><span class="p">),</span></span><a href="#l188"></a>
<span id="l189">        <span class="n">follow_symlinks</span><span class="o">=</span><span class="n">follow</span><span class="p">)</span></span><a href="#l189"></a>
<span id="l190">    <span class="k">try</span><span class="p">:</span></span><a href="#l190"></a>
<span id="l191">        <span class="n">lookup</span><span class="p">(</span><span class="s">&quot;chmod&quot;</span><span class="p">)(</span><span class="n">dst</span><span class="p">,</span> <span class="n">mode</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="n">follow</span><span class="p">)</span></span><a href="#l191"></a>
<span id="l192">    <span class="k">except</span> <span class="ne">NotImplementedError</span><span class="p">:</span></span><a href="#l192"></a>
<span id="l193">        <span class="c"># if we got a NotImplementedError, it&#39;s because</span></span><a href="#l193"></a>
<span id="l194">        <span class="c">#   * follow_symlinks=False,</span></span><a href="#l194"></a>
<span id="l195">        <span class="c">#   * lchown() is unavailable, and</span></span><a href="#l195"></a>
<span id="l196">        <span class="c">#   * either</span></span><a href="#l196"></a>
<span id="l197">        <span class="c">#       * fchownat() is unavailable or</span></span><a href="#l197"></a>
<span id="l198">        <span class="c">#       * fchownat() doesn&#39;t implement AT_SYMLINK_NOFOLLOW.</span></span><a href="#l198"></a>
<span id="l199">        <span class="c">#         (it returned ENOSUP.)</span></span><a href="#l199"></a>
<span id="l200">        <span class="c"># therefore we&#39;re out of options--we simply cannot chown the</span></span><a href="#l200"></a>
<span id="l201">        <span class="c"># symlink.  give up, suppress the error.</span></span><a href="#l201"></a>
<span id="l202">        <span class="c"># (which is what shutil always did in this circumstance.)</span></span><a href="#l202"></a>
<span id="l203">        <span class="k">pass</span></span><a href="#l203"></a>
<span id="l204">    <span class="k">if</span> <span class="nb">hasattr</span><span class="p">(</span><span class="n">st</span><span class="p">,</span> <span class="s">&#39;st_flags&#39;</span><span class="p">):</span></span><a href="#l204"></a>
<span id="l205">        <span class="k">try</span><span class="p">:</span></span><a href="#l205"></a>
<span id="l206">            <span class="n">lookup</span><span class="p">(</span><span class="s">&quot;chflags&quot;</span><span class="p">)(</span><span class="n">dst</span><span class="p">,</span> <span class="n">st</span><span class="o">.</span><span class="n">st_flags</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="n">follow</span><span class="p">)</span></span><a href="#l206"></a>
<span id="l207">        <span class="k">except</span> <span class="ne">OSError</span> <span class="k">as</span> <span class="n">why</span><span class="p">:</span></span><a href="#l207"></a>
<span id="l208">            <span class="k">for</span> <span class="n">err</span> <span class="ow">in</span> <span class="s">&#39;EOPNOTSUPP&#39;</span><span class="p">,</span> <span class="s">&#39;ENOTSUP&#39;</span><span class="p">:</span></span><a href="#l208"></a>
<span id="l209">                <span class="k">if</span> <span class="nb">hasattr</span><span class="p">(</span><span class="n">errno</span><span class="p">,</span> <span class="n">err</span><span class="p">)</span> <span class="ow">and</span> <span class="n">why</span><span class="o">.</span><span class="n">errno</span> <span class="o">==</span> <span class="nb">getattr</span><span class="p">(</span><span class="n">errno</span><span class="p">,</span> <span class="n">err</span><span class="p">):</span></span><a href="#l209"></a>
<span id="l210">                    <span class="k">break</span></span><a href="#l210"></a>
<span id="l211">            <span class="k">else</span><span class="p">:</span></span><a href="#l211"></a>
<span id="l212">                <span class="k">raise</span></span><a href="#l212"></a>
<span id="l213">    <span class="n">_copyxattr</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="n">follow</span><span class="p">)</span></span><a href="#l213"></a>
<span id="l214"></span><a href="#l214"></a>
<span id="l215"><span class="k">def</span> <span class="nf">copy</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">,</span> <span class="o">*</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="bp">True</span><span class="p">):</span></span><a href="#l215"></a>
<span id="l216">    <span class="sd">&quot;&quot;&quot;Copy data and mode bits (&quot;cp src dst&quot;). Return the file&#39;s destination.</span></span><a href="#l216"></a>
<span id="l217"></span><a href="#l217"></a>
<span id="l218"><span class="sd">    The destination may be a directory.</span></span><a href="#l218"></a>
<span id="l219"></span><a href="#l219"></a>
<span id="l220"><span class="sd">    If follow_symlinks is false, symlinks won&#39;t be followed. This</span></span><a href="#l220"></a>
<span id="l221"><span class="sd">    resembles GNU&#39;s &quot;cp -P src dst&quot;.</span></span><a href="#l221"></a>
<span id="l222"></span><a href="#l222"></a>
<span id="l223"><span class="sd">    If source and destination are the same file, a SameFileError will be</span></span><a href="#l223"></a>
<span id="l224"><span class="sd">    raised.</span></span><a href="#l224"></a>
<span id="l225"></span><a href="#l225"></a>
<span id="l226"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l226"></a>
<span id="l227">    <span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">isdir</span><span class="p">(</span><span class="n">dst</span><span class="p">):</span></span><a href="#l227"></a>
<span id="l228">        <span class="n">dst</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">dst</span><span class="p">,</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">basename</span><span class="p">(</span><span class="n">src</span><span class="p">))</span></span><a href="#l228"></a>
<span id="l229">    <span class="n">copyfile</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="n">follow_symlinks</span><span class="p">)</span></span><a href="#l229"></a>
<span id="l230">    <span class="n">copymode</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="n">follow_symlinks</span><span class="p">)</span></span><a href="#l230"></a>
<span id="l231">    <span class="k">return</span> <span class="n">dst</span></span><a href="#l231"></a>
<span id="l232"></span><a href="#l232"></a>
<span id="l233"><span class="k">def</span> <span class="nf">copy2</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">,</span> <span class="o">*</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="bp">True</span><span class="p">):</span></span><a href="#l233"></a>
<span id="l234">    <span class="sd">&quot;&quot;&quot;Copy data and all stat info (&quot;cp -p src dst&quot;). Return the file&#39;s</span></span><a href="#l234"></a>
<span id="l235"><span class="sd">    destination.&quot;</span></span><a href="#l235"></a>
<span id="l236"></span><a href="#l236"></a>
<span id="l237"><span class="sd">    The destination may be a directory.</span></span><a href="#l237"></a>
<span id="l238"></span><a href="#l238"></a>
<span id="l239"><span class="sd">    If follow_symlinks is false, symlinks won&#39;t be followed. This</span></span><a href="#l239"></a>
<span id="l240"><span class="sd">    resembles GNU&#39;s &quot;cp -P src dst&quot;.</span></span><a href="#l240"></a>
<span id="l241"></span><a href="#l241"></a>
<span id="l242"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l242"></a>
<span id="l243">    <span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">isdir</span><span class="p">(</span><span class="n">dst</span><span class="p">):</span></span><a href="#l243"></a>
<span id="l244">        <span class="n">dst</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">dst</span><span class="p">,</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">basename</span><span class="p">(</span><span class="n">src</span><span class="p">))</span></span><a href="#l244"></a>
<span id="l245">    <span class="n">copyfile</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="n">follow_symlinks</span><span class="p">)</span></span><a href="#l245"></a>
<span id="l246">    <span class="n">copystat</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="n">follow_symlinks</span><span class="p">)</span></span><a href="#l246"></a>
<span id="l247">    <span class="k">return</span> <span class="n">dst</span></span><a href="#l247"></a>
<span id="l248"></span><a href="#l248"></a>
<span id="l249"><span class="k">def</span> <span class="nf">ignore_patterns</span><span class="p">(</span><span class="o">*</span><span class="n">patterns</span><span class="p">):</span></span><a href="#l249"></a>
<span id="l250">    <span class="sd">&quot;&quot;&quot;Function that can be used as copytree() ignore parameter.</span></span><a href="#l250"></a>
<span id="l251"></span><a href="#l251"></a>
<span id="l252"><span class="sd">    Patterns is a sequence of glob-style patterns</span></span><a href="#l252"></a>
<span id="l253"><span class="sd">    that are used to exclude files&quot;&quot;&quot;</span></span><a href="#l253"></a>
<span id="l254">    <span class="k">def</span> <span class="nf">_ignore_patterns</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">names</span><span class="p">):</span></span><a href="#l254"></a>
<span id="l255">        <span class="n">ignored_names</span> <span class="o">=</span> <span class="p">[]</span></span><a href="#l255"></a>
<span id="l256">        <span class="k">for</span> <span class="n">pattern</span> <span class="ow">in</span> <span class="n">patterns</span><span class="p">:</span></span><a href="#l256"></a>
<span id="l257">            <span class="n">ignored_names</span><span class="o">.</span><span class="n">extend</span><span class="p">(</span><span class="n">fnmatch</span><span class="o">.</span><span class="n">filter</span><span class="p">(</span><span class="n">names</span><span class="p">,</span> <span class="n">pattern</span><span class="p">))</span></span><a href="#l257"></a>
<span id="l258">        <span class="k">return</span> <span class="nb">set</span><span class="p">(</span><span class="n">ignored_names</span><span class="p">)</span></span><a href="#l258"></a>
<span id="l259">    <span class="k">return</span> <span class="n">_ignore_patterns</span></span><a href="#l259"></a>
<span id="l260"></span><a href="#l260"></a>
<span id="l261"><span class="k">def</span> <span class="nf">copytree</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">,</span> <span class="n">symlinks</span><span class="o">=</span><span class="bp">False</span><span class="p">,</span> <span class="n">ignore</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="n">copy_function</span><span class="o">=</span><span class="n">copy2</span><span class="p">,</span></span><a href="#l261"></a>
<span id="l262">             <span class="n">ignore_dangling_symlinks</span><span class="o">=</span><span class="bp">False</span><span class="p">):</span></span><a href="#l262"></a>
<span id="l263">    <span class="sd">&quot;&quot;&quot;Recursively copy a directory tree.</span></span><a href="#l263"></a>
<span id="l264"></span><a href="#l264"></a>
<span id="l265"><span class="sd">    The destination directory must not already exist.</span></span><a href="#l265"></a>
<span id="l266"><span class="sd">    If exception(s) occur, an Error is raised with a list of reasons.</span></span><a href="#l266"></a>
<span id="l267"></span><a href="#l267"></a>
<span id="l268"><span class="sd">    If the optional symlinks flag is true, symbolic links in the</span></span><a href="#l268"></a>
<span id="l269"><span class="sd">    source tree result in symbolic links in the destination tree; if</span></span><a href="#l269"></a>
<span id="l270"><span class="sd">    it is false, the contents of the files pointed to by symbolic</span></span><a href="#l270"></a>
<span id="l271"><span class="sd">    links are copied. If the file pointed by the symlink doesn&#39;t</span></span><a href="#l271"></a>
<span id="l272"><span class="sd">    exist, an exception will be added in the list of errors raised in</span></span><a href="#l272"></a>
<span id="l273"><span class="sd">    an Error exception at the end of the copy process.</span></span><a href="#l273"></a>
<span id="l274"></span><a href="#l274"></a>
<span id="l275"><span class="sd">    You can set the optional ignore_dangling_symlinks flag to true if you</span></span><a href="#l275"></a>
<span id="l276"><span class="sd">    want to silence this exception. Notice that this has no effect on</span></span><a href="#l276"></a>
<span id="l277"><span class="sd">    platforms that don&#39;t support os.symlink.</span></span><a href="#l277"></a>
<span id="l278"></span><a href="#l278"></a>
<span id="l279"><span class="sd">    The optional ignore argument is a callable. If given, it</span></span><a href="#l279"></a>
<span id="l280"><span class="sd">    is called with the `src` parameter, which is the directory</span></span><a href="#l280"></a>
<span id="l281"><span class="sd">    being visited by copytree(), and `names` which is the list of</span></span><a href="#l281"></a>
<span id="l282"><span class="sd">    `src` contents, as returned by os.listdir():</span></span><a href="#l282"></a>
<span id="l283"></span><a href="#l283"></a>
<span id="l284"><span class="sd">        callable(src, names) -&gt; ignored_names</span></span><a href="#l284"></a>
<span id="l285"></span><a href="#l285"></a>
<span id="l286"><span class="sd">    Since copytree() is called recursively, the callable will be</span></span><a href="#l286"></a>
<span id="l287"><span class="sd">    called once for each directory that is copied. It returns a</span></span><a href="#l287"></a>
<span id="l288"><span class="sd">    list of names relative to the `src` directory that should</span></span><a href="#l288"></a>
<span id="l289"><span class="sd">    not be copied.</span></span><a href="#l289"></a>
<span id="l290"></span><a href="#l290"></a>
<span id="l291"><span class="sd">    The optional copy_function argument is a callable that will be used</span></span><a href="#l291"></a>
<span id="l292"><span class="sd">    to copy each file. It will be called with the source path and the</span></span><a href="#l292"></a>
<span id="l293"><span class="sd">    destination path as arguments. By default, copy2() is used, but any</span></span><a href="#l293"></a>
<span id="l294"><span class="sd">    function that supports the same signature (like copy()) can be used.</span></span><a href="#l294"></a>
<span id="l295"></span><a href="#l295"></a>
<span id="l296"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l296"></a>
<span id="l297">    <span class="n">names</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">listdir</span><span class="p">(</span><span class="n">src</span><span class="p">)</span></span><a href="#l297"></a>
<span id="l298">    <span class="k">if</span> <span class="n">ignore</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l298"></a>
<span id="l299">        <span class="n">ignored_names</span> <span class="o">=</span> <span class="n">ignore</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">names</span><span class="p">)</span></span><a href="#l299"></a>
<span id="l300">    <span class="k">else</span><span class="p">:</span></span><a href="#l300"></a>
<span id="l301">        <span class="n">ignored_names</span> <span class="o">=</span> <span class="nb">set</span><span class="p">()</span></span><a href="#l301"></a>
<span id="l302"></span><a href="#l302"></a>
<span id="l303">    <span class="n">os</span><span class="o">.</span><span class="n">makedirs</span><span class="p">(</span><span class="n">dst</span><span class="p">)</span></span><a href="#l303"></a>
<span id="l304">    <span class="n">errors</span> <span class="o">=</span> <span class="p">[]</span></span><a href="#l304"></a>
<span id="l305">    <span class="k">for</span> <span class="n">name</span> <span class="ow">in</span> <span class="n">names</span><span class="p">:</span></span><a href="#l305"></a>
<span id="l306">        <span class="k">if</span> <span class="n">name</span> <span class="ow">in</span> <span class="n">ignored_names</span><span class="p">:</span></span><a href="#l306"></a>
<span id="l307">            <span class="k">continue</span></span><a href="#l307"></a>
<span id="l308">        <span class="n">srcname</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">name</span><span class="p">)</span></span><a href="#l308"></a>
<span id="l309">        <span class="n">dstname</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">dst</span><span class="p">,</span> <span class="n">name</span><span class="p">)</span></span><a href="#l309"></a>
<span id="l310">        <span class="k">try</span><span class="p">:</span></span><a href="#l310"></a>
<span id="l311">            <span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">islink</span><span class="p">(</span><span class="n">srcname</span><span class="p">):</span></span><a href="#l311"></a>
<span id="l312">                <span class="n">linkto</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">readlink</span><span class="p">(</span><span class="n">srcname</span><span class="p">)</span></span><a href="#l312"></a>
<span id="l313">                <span class="k">if</span> <span class="n">symlinks</span><span class="p">:</span></span><a href="#l313"></a>
<span id="l314">                    <span class="c"># We can&#39;t just leave it to `copy_function` because legacy</span></span><a href="#l314"></a>
<span id="l315">                    <span class="c"># code with a custom `copy_function` may rely on copytree</span></span><a href="#l315"></a>
<span id="l316">                    <span class="c"># doing the right thing.</span></span><a href="#l316"></a>
<span id="l317">                    <span class="n">os</span><span class="o">.</span><span class="n">symlink</span><span class="p">(</span><span class="n">linkto</span><span class="p">,</span> <span class="n">dstname</span><span class="p">)</span></span><a href="#l317"></a>
<span id="l318">                    <span class="n">copystat</span><span class="p">(</span><span class="n">srcname</span><span class="p">,</span> <span class="n">dstname</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="ow">not</span> <span class="n">symlinks</span><span class="p">)</span></span><a href="#l318"></a>
<span id="l319">                <span class="k">else</span><span class="p">:</span></span><a href="#l319"></a>
<span id="l320">                    <span class="c"># ignore dangling symlink if the flag is on</span></span><a href="#l320"></a>
<span id="l321">                    <span class="k">if</span> <span class="ow">not</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">exists</span><span class="p">(</span><span class="n">linkto</span><span class="p">)</span> <span class="ow">and</span> <span class="n">ignore_dangling_symlinks</span><span class="p">:</span></span><a href="#l321"></a>
<span id="l322">                        <span class="k">continue</span></span><a href="#l322"></a>
<span id="l323">                    <span class="c"># otherwise let the copy occurs. copy2 will raise an error</span></span><a href="#l323"></a>
<span id="l324">                    <span class="n">copy_function</span><span class="p">(</span><span class="n">srcname</span><span class="p">,</span> <span class="n">dstname</span><span class="p">)</span></span><a href="#l324"></a>
<span id="l325">            <span class="k">elif</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">isdir</span><span class="p">(</span><span class="n">srcname</span><span class="p">):</span></span><a href="#l325"></a>
<span id="l326">                <span class="n">copytree</span><span class="p">(</span><span class="n">srcname</span><span class="p">,</span> <span class="n">dstname</span><span class="p">,</span> <span class="n">symlinks</span><span class="p">,</span> <span class="n">ignore</span><span class="p">,</span> <span class="n">copy_function</span><span class="p">)</span></span><a href="#l326"></a>
<span id="l327">            <span class="k">else</span><span class="p">:</span></span><a href="#l327"></a>
<span id="l328">                <span class="c"># Will raise a SpecialFileError for unsupported file types</span></span><a href="#l328"></a>
<span id="l329">                <span class="n">copy_function</span><span class="p">(</span><span class="n">srcname</span><span class="p">,</span> <span class="n">dstname</span><span class="p">)</span></span><a href="#l329"></a>
<span id="l330">        <span class="c"># catch the Error from the recursive copytree so that we can</span></span><a href="#l330"></a>
<span id="l331">        <span class="c"># continue with other files</span></span><a href="#l331"></a>
<span id="l332">        <span class="k">except</span> <span class="n">Error</span> <span class="k">as</span> <span class="n">err</span><span class="p">:</span></span><a href="#l332"></a>
<span id="l333">            <span class="n">errors</span><span class="o">.</span><span class="n">extend</span><span class="p">(</span><span class="n">err</span><span class="o">.</span><span class="n">args</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span></span><a href="#l333"></a>
<span id="l334">        <span class="k">except</span> <span class="ne">OSError</span> <span class="k">as</span> <span class="n">why</span><span class="p">:</span></span><a href="#l334"></a>
<span id="l335">            <span class="n">errors</span><span class="o">.</span><span class="n">append</span><span class="p">((</span><span class="n">srcname</span><span class="p">,</span> <span class="n">dstname</span><span class="p">,</span> <span class="nb">str</span><span class="p">(</span><span class="n">why</span><span class="p">)))</span></span><a href="#l335"></a>
<span id="l336">    <span class="k">try</span><span class="p">:</span></span><a href="#l336"></a>
<span id="l337">        <span class="n">copystat</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">)</span></span><a href="#l337"></a>
<span id="l338">    <span class="k">except</span> <span class="ne">OSError</span> <span class="k">as</span> <span class="n">why</span><span class="p">:</span></span><a href="#l338"></a>
<span id="l339">        <span class="c"># Copying file access times may fail on Windows</span></span><a href="#l339"></a>
<span id="l340">        <span class="k">if</span> <span class="nb">getattr</span><span class="p">(</span><span class="n">why</span><span class="p">,</span> <span class="s">&#39;winerror&#39;</span><span class="p">,</span> <span class="bp">None</span><span class="p">)</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l340"></a>
<span id="l341">            <span class="n">errors</span><span class="o">.</span><span class="n">append</span><span class="p">((</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">,</span> <span class="nb">str</span><span class="p">(</span><span class="n">why</span><span class="p">)))</span></span><a href="#l341"></a>
<span id="l342">    <span class="k">if</span> <span class="n">errors</span><span class="p">:</span></span><a href="#l342"></a>
<span id="l343">        <span class="k">raise</span> <span class="n">Error</span><span class="p">(</span><span class="n">errors</span><span class="p">)</span></span><a href="#l343"></a>
<span id="l344">    <span class="k">return</span> <span class="n">dst</span></span><a href="#l344"></a>
<span id="l345"></span><a href="#l345"></a>
<span id="l346"><span class="c"># version vulnerable to race conditions</span></span><a href="#l346"></a>
<span id="l347"><span class="k">def</span> <span class="nf">_rmtree_unsafe</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">onerror</span><span class="p">):</span></span><a href="#l347"></a>
<span id="l348">    <span class="k">try</span><span class="p">:</span></span><a href="#l348"></a>
<span id="l349">        <span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">islink</span><span class="p">(</span><span class="n">path</span><span class="p">):</span></span><a href="#l349"></a>
<span id="l350">            <span class="c"># symlinks to directories are forbidden, see bug #1669</span></span><a href="#l350"></a>
<span id="l351">            <span class="k">raise</span> <span class="ne">OSError</span><span class="p">(</span><span class="s">&quot;Cannot call rmtree on a symbolic link&quot;</span><span class="p">)</span></span><a href="#l351"></a>
<span id="l352">    <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l352"></a>
<span id="l353">        <span class="n">onerror</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">islink</span><span class="p">,</span> <span class="n">path</span><span class="p">,</span> <span class="n">sys</span><span class="o">.</span><span class="n">exc_info</span><span class="p">())</span></span><a href="#l353"></a>
<span id="l354">        <span class="c"># can&#39;t continue even if onerror hook returns</span></span><a href="#l354"></a>
<span id="l355">        <span class="k">return</span></span><a href="#l355"></a>
<span id="l356">    <span class="n">names</span> <span class="o">=</span> <span class="p">[]</span></span><a href="#l356"></a>
<span id="l357">    <span class="k">try</span><span class="p">:</span></span><a href="#l357"></a>
<span id="l358">        <span class="n">names</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">listdir</span><span class="p">(</span><span class="n">path</span><span class="p">)</span></span><a href="#l358"></a>
<span id="l359">    <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l359"></a>
<span id="l360">        <span class="n">onerror</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">listdir</span><span class="p">,</span> <span class="n">path</span><span class="p">,</span> <span class="n">sys</span><span class="o">.</span><span class="n">exc_info</span><span class="p">())</span></span><a href="#l360"></a>
<span id="l361">    <span class="k">for</span> <span class="n">name</span> <span class="ow">in</span> <span class="n">names</span><span class="p">:</span></span><a href="#l361"></a>
<span id="l362">        <span class="n">fullname</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">name</span><span class="p">)</span></span><a href="#l362"></a>
<span id="l363">        <span class="k">try</span><span class="p">:</span></span><a href="#l363"></a>
<span id="l364">            <span class="n">mode</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">lstat</span><span class="p">(</span><span class="n">fullname</span><span class="p">)</span><span class="o">.</span><span class="n">st_mode</span></span><a href="#l364"></a>
<span id="l365">        <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l365"></a>
<span id="l366">            <span class="n">mode</span> <span class="o">=</span> <span class="mi">0</span></span><a href="#l366"></a>
<span id="l367">        <span class="k">if</span> <span class="n">stat</span><span class="o">.</span><span class="n">S_ISDIR</span><span class="p">(</span><span class="n">mode</span><span class="p">):</span></span><a href="#l367"></a>
<span id="l368">            <span class="n">_rmtree_unsafe</span><span class="p">(</span><span class="n">fullname</span><span class="p">,</span> <span class="n">onerror</span><span class="p">)</span></span><a href="#l368"></a>
<span id="l369">        <span class="k">else</span><span class="p">:</span></span><a href="#l369"></a>
<span id="l370">            <span class="k">try</span><span class="p">:</span></span><a href="#l370"></a>
<span id="l371">                <span class="n">os</span><span class="o">.</span><span class="n">unlink</span><span class="p">(</span><span class="n">fullname</span><span class="p">)</span></span><a href="#l371"></a>
<span id="l372">            <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l372"></a>
<span id="l373">                <span class="n">onerror</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">unlink</span><span class="p">,</span> <span class="n">fullname</span><span class="p">,</span> <span class="n">sys</span><span class="o">.</span><span class="n">exc_info</span><span class="p">())</span></span><a href="#l373"></a>
<span id="l374">    <span class="k">try</span><span class="p">:</span></span><a href="#l374"></a>
<span id="l375">        <span class="n">os</span><span class="o">.</span><span class="n">rmdir</span><span class="p">(</span><span class="n">path</span><span class="p">)</span></span><a href="#l375"></a>
<span id="l376">    <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l376"></a>
<span id="l377">        <span class="n">onerror</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">rmdir</span><span class="p">,</span> <span class="n">path</span><span class="p">,</span> <span class="n">sys</span><span class="o">.</span><span class="n">exc_info</span><span class="p">())</span></span><a href="#l377"></a>
<span id="l378"></span><a href="#l378"></a>
<span id="l379"><span class="c"># Version using fd-based APIs to protect against races</span></span><a href="#l379"></a>
<span id="l380"><span class="k">def</span> <span class="nf">_rmtree_safe_fd</span><span class="p">(</span><span class="n">topfd</span><span class="p">,</span> <span class="n">path</span><span class="p">,</span> <span class="n">onerror</span><span class="p">):</span></span><a href="#l380"></a>
<span id="l381">    <span class="n">names</span> <span class="o">=</span> <span class="p">[]</span></span><a href="#l381"></a>
<span id="l382">    <span class="k">try</span><span class="p">:</span></span><a href="#l382"></a>
<span id="l383">        <span class="n">names</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">listdir</span><span class="p">(</span><span class="n">topfd</span><span class="p">)</span></span><a href="#l383"></a>
<span id="l384">    <span class="k">except</span> <span class="ne">OSError</span> <span class="k">as</span> <span class="n">err</span><span class="p">:</span></span><a href="#l384"></a>
<span id="l385">        <span class="n">err</span><span class="o">.</span><span class="n">filename</span> <span class="o">=</span> <span class="n">path</span></span><a href="#l385"></a>
<span id="l386">        <span class="n">onerror</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">listdir</span><span class="p">,</span> <span class="n">path</span><span class="p">,</span> <span class="n">sys</span><span class="o">.</span><span class="n">exc_info</span><span class="p">())</span></span><a href="#l386"></a>
<span id="l387">    <span class="k">for</span> <span class="n">name</span> <span class="ow">in</span> <span class="n">names</span><span class="p">:</span></span><a href="#l387"></a>
<span id="l388">        <span class="n">fullname</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">name</span><span class="p">)</span></span><a href="#l388"></a>
<span id="l389">        <span class="k">try</span><span class="p">:</span></span><a href="#l389"></a>
<span id="l390">            <span class="n">orig_st</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">stat</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="n">dir_fd</span><span class="o">=</span><span class="n">topfd</span><span class="p">,</span> <span class="n">follow_symlinks</span><span class="o">=</span><span class="bp">False</span><span class="p">)</span></span><a href="#l390"></a>
<span id="l391">            <span class="n">mode</span> <span class="o">=</span> <span class="n">orig_st</span><span class="o">.</span><span class="n">st_mode</span></span><a href="#l391"></a>
<span id="l392">        <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l392"></a>
<span id="l393">            <span class="n">mode</span> <span class="o">=</span> <span class="mi">0</span></span><a href="#l393"></a>
<span id="l394">        <span class="k">if</span> <span class="n">stat</span><span class="o">.</span><span class="n">S_ISDIR</span><span class="p">(</span><span class="n">mode</span><span class="p">):</span></span><a href="#l394"></a>
<span id="l395">            <span class="k">try</span><span class="p">:</span></span><a href="#l395"></a>
<span id="l396">                <span class="n">dirfd</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">open</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="n">os</span><span class="o">.</span><span class="n">O_RDONLY</span><span class="p">,</span> <span class="n">dir_fd</span><span class="o">=</span><span class="n">topfd</span><span class="p">)</span></span><a href="#l396"></a>
<span id="l397">            <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l397"></a>
<span id="l398">                <span class="n">onerror</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">open</span><span class="p">,</span> <span class="n">fullname</span><span class="p">,</span> <span class="n">sys</span><span class="o">.</span><span class="n">exc_info</span><span class="p">())</span></span><a href="#l398"></a>
<span id="l399">            <span class="k">else</span><span class="p">:</span></span><a href="#l399"></a>
<span id="l400">                <span class="k">try</span><span class="p">:</span></span><a href="#l400"></a>
<span id="l401">                    <span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">samestat</span><span class="p">(</span><span class="n">orig_st</span><span class="p">,</span> <span class="n">os</span><span class="o">.</span><span class="n">fstat</span><span class="p">(</span><span class="n">dirfd</span><span class="p">)):</span></span><a href="#l401"></a>
<span id="l402">                        <span class="n">_rmtree_safe_fd</span><span class="p">(</span><span class="n">dirfd</span><span class="p">,</span> <span class="n">fullname</span><span class="p">,</span> <span class="n">onerror</span><span class="p">)</span></span><a href="#l402"></a>
<span id="l403">                        <span class="k">try</span><span class="p">:</span></span><a href="#l403"></a>
<span id="l404">                            <span class="n">os</span><span class="o">.</span><span class="n">rmdir</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="n">dir_fd</span><span class="o">=</span><span class="n">topfd</span><span class="p">)</span></span><a href="#l404"></a>
<span id="l405">                        <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l405"></a>
<span id="l406">                            <span class="n">onerror</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">rmdir</span><span class="p">,</span> <span class="n">fullname</span><span class="p">,</span> <span class="n">sys</span><span class="o">.</span><span class="n">exc_info</span><span class="p">())</span></span><a href="#l406"></a>
<span id="l407">                    <span class="k">else</span><span class="p">:</span></span><a href="#l407"></a>
<span id="l408">                        <span class="k">try</span><span class="p">:</span></span><a href="#l408"></a>
<span id="l409">                            <span class="c"># This can only happen if someone replaces</span></span><a href="#l409"></a>
<span id="l410">                            <span class="c"># a directory with a symlink after the call to</span></span><a href="#l410"></a>
<span id="l411">                            <span class="c"># stat.S_ISDIR above.</span></span><a href="#l411"></a>
<span id="l412">                            <span class="k">raise</span> <span class="ne">OSError</span><span class="p">(</span><span class="s">&quot;Cannot call rmtree on a symbolic &quot;</span></span><a href="#l412"></a>
<span id="l413">                                          <span class="s">&quot;link&quot;</span><span class="p">)</span></span><a href="#l413"></a>
<span id="l414">                        <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l414"></a>
<span id="l415">                            <span class="n">onerror</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">islink</span><span class="p">,</span> <span class="n">fullname</span><span class="p">,</span> <span class="n">sys</span><span class="o">.</span><span class="n">exc_info</span><span class="p">())</span></span><a href="#l415"></a>
<span id="l416">                <span class="k">finally</span><span class="p">:</span></span><a href="#l416"></a>
<span id="l417">                    <span class="n">os</span><span class="o">.</span><span class="n">close</span><span class="p">(</span><span class="n">dirfd</span><span class="p">)</span></span><a href="#l417"></a>
<span id="l418">        <span class="k">else</span><span class="p">:</span></span><a href="#l418"></a>
<span id="l419">            <span class="k">try</span><span class="p">:</span></span><a href="#l419"></a>
<span id="l420">                <span class="n">os</span><span class="o">.</span><span class="n">unlink</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="n">dir_fd</span><span class="o">=</span><span class="n">topfd</span><span class="p">)</span></span><a href="#l420"></a>
<span id="l421">            <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l421"></a>
<span id="l422">                <span class="n">onerror</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">unlink</span><span class="p">,</span> <span class="n">fullname</span><span class="p">,</span> <span class="n">sys</span><span class="o">.</span><span class="n">exc_info</span><span class="p">())</span></span><a href="#l422"></a>
<span id="l423"></span><a href="#l423"></a>
<span id="l424"><span class="n">_use_fd_functions</span> <span class="o">=</span> <span class="p">({</span><span class="n">os</span><span class="o">.</span><span class="n">open</span><span class="p">,</span> <span class="n">os</span><span class="o">.</span><span class="n">stat</span><span class="p">,</span> <span class="n">os</span><span class="o">.</span><span class="n">unlink</span><span class="p">,</span> <span class="n">os</span><span class="o">.</span><span class="n">rmdir</span><span class="p">}</span> <span class="o">&lt;=</span></span><a href="#l424"></a>
<span id="l425">                     <span class="n">os</span><span class="o">.</span><span class="n">supports_dir_fd</span> <span class="ow">and</span></span><a href="#l425"></a>
<span id="l426">                     <span class="n">os</span><span class="o">.</span><span class="n">listdir</span> <span class="ow">in</span> <span class="n">os</span><span class="o">.</span><span class="n">supports_fd</span> <span class="ow">and</span></span><a href="#l426"></a>
<span id="l427">                     <span class="n">os</span><span class="o">.</span><span class="n">stat</span> <span class="ow">in</span> <span class="n">os</span><span class="o">.</span><span class="n">supports_follow_symlinks</span><span class="p">)</span></span><a href="#l427"></a>
<span id="l428"></span><a href="#l428"></a>
<span id="l429"><span class="k">def</span> <span class="nf">rmtree</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">ignore_errors</span><span class="o">=</span><span class="bp">False</span><span class="p">,</span> <span class="n">onerror</span><span class="o">=</span><span class="bp">None</span><span class="p">):</span></span><a href="#l429"></a>
<span id="l430">    <span class="sd">&quot;&quot;&quot;Recursively delete a directory tree.</span></span><a href="#l430"></a>
<span id="l431"></span><a href="#l431"></a>
<span id="l432"><span class="sd">    If ignore_errors is set, errors are ignored; otherwise, if onerror</span></span><a href="#l432"></a>
<span id="l433"><span class="sd">    is set, it is called to handle the error with arguments (func,</span></span><a href="#l433"></a>
<span id="l434"><span class="sd">    path, exc_info) where func is platform and implementation dependent;</span></span><a href="#l434"></a>
<span id="l435"><span class="sd">    path is the argument to that function that caused it to fail; and</span></span><a href="#l435"></a>
<span id="l436"><span class="sd">    exc_info is a tuple returned by sys.exc_info().  If ignore_errors</span></span><a href="#l436"></a>
<span id="l437"><span class="sd">    is false and onerror is None, an exception is raised.</span></span><a href="#l437"></a>
<span id="l438"></span><a href="#l438"></a>
<span id="l439"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l439"></a>
<span id="l440">    <span class="k">if</span> <span class="n">ignore_errors</span><span class="p">:</span></span><a href="#l440"></a>
<span id="l441">        <span class="k">def</span> <span class="nf">onerror</span><span class="p">(</span><span class="o">*</span><span class="n">args</span><span class="p">):</span></span><a href="#l441"></a>
<span id="l442">            <span class="k">pass</span></span><a href="#l442"></a>
<span id="l443">    <span class="k">elif</span> <span class="n">onerror</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l443"></a>
<span id="l444">        <span class="k">def</span> <span class="nf">onerror</span><span class="p">(</span><span class="o">*</span><span class="n">args</span><span class="p">):</span></span><a href="#l444"></a>
<span id="l445">            <span class="k">raise</span></span><a href="#l445"></a>
<span id="l446">    <span class="k">if</span> <span class="n">_use_fd_functions</span><span class="p">:</span></span><a href="#l446"></a>
<span id="l447">        <span class="c"># While the unsafe rmtree works fine on bytes, the fd based does not.</span></span><a href="#l447"></a>
<span id="l448">        <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="nb">bytes</span><span class="p">):</span></span><a href="#l448"></a>
<span id="l449">            <span class="n">path</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">fsdecode</span><span class="p">(</span><span class="n">path</span><span class="p">)</span></span><a href="#l449"></a>
<span id="l450">        <span class="c"># Note: To guard against symlink races, we use the standard</span></span><a href="#l450"></a>
<span id="l451">        <span class="c"># lstat()/open()/fstat() trick.</span></span><a href="#l451"></a>
<span id="l452">        <span class="k">try</span><span class="p">:</span></span><a href="#l452"></a>
<span id="l453">            <span class="n">orig_st</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">lstat</span><span class="p">(</span><span class="n">path</span><span class="p">)</span></span><a href="#l453"></a>
<span id="l454">        <span class="k">except</span> <span class="ne">Exception</span><span class="p">:</span></span><a href="#l454"></a>
<span id="l455">            <span class="n">onerror</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">lstat</span><span class="p">,</span> <span class="n">path</span><span class="p">,</span> <span class="n">sys</span><span class="o">.</span><span class="n">exc_info</span><span class="p">())</span></span><a href="#l455"></a>
<span id="l456">            <span class="k">return</span></span><a href="#l456"></a>
<span id="l457">        <span class="k">try</span><span class="p">:</span></span><a href="#l457"></a>
<span id="l458">            <span class="n">fd</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">open</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">os</span><span class="o">.</span><span class="n">O_RDONLY</span><span class="p">)</span></span><a href="#l458"></a>
<span id="l459">        <span class="k">except</span> <span class="ne">Exception</span><span class="p">:</span></span><a href="#l459"></a>
<span id="l460">            <span class="n">onerror</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">lstat</span><span class="p">,</span> <span class="n">path</span><span class="p">,</span> <span class="n">sys</span><span class="o">.</span><span class="n">exc_info</span><span class="p">())</span></span><a href="#l460"></a>
<span id="l461">            <span class="k">return</span></span><a href="#l461"></a>
<span id="l462">        <span class="k">try</span><span class="p">:</span></span><a href="#l462"></a>
<span id="l463">            <span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">samestat</span><span class="p">(</span><span class="n">orig_st</span><span class="p">,</span> <span class="n">os</span><span class="o">.</span><span class="n">fstat</span><span class="p">(</span><span class="n">fd</span><span class="p">)):</span></span><a href="#l463"></a>
<span id="l464">                <span class="n">_rmtree_safe_fd</span><span class="p">(</span><span class="n">fd</span><span class="p">,</span> <span class="n">path</span><span class="p">,</span> <span class="n">onerror</span><span class="p">)</span></span><a href="#l464"></a>
<span id="l465">                <span class="k">try</span><span class="p">:</span></span><a href="#l465"></a>
<span id="l466">                    <span class="n">os</span><span class="o">.</span><span class="n">rmdir</span><span class="p">(</span><span class="n">path</span><span class="p">)</span></span><a href="#l466"></a>
<span id="l467">                <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l467"></a>
<span id="l468">                    <span class="n">onerror</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">rmdir</span><span class="p">,</span> <span class="n">path</span><span class="p">,</span> <span class="n">sys</span><span class="o">.</span><span class="n">exc_info</span><span class="p">())</span></span><a href="#l468"></a>
<span id="l469">            <span class="k">else</span><span class="p">:</span></span><a href="#l469"></a>
<span id="l470">                <span class="k">try</span><span class="p">:</span></span><a href="#l470"></a>
<span id="l471">                    <span class="c"># symlinks to directories are forbidden, see bug #1669</span></span><a href="#l471"></a>
<span id="l472">                    <span class="k">raise</span> <span class="ne">OSError</span><span class="p">(</span><span class="s">&quot;Cannot call rmtree on a symbolic link&quot;</span><span class="p">)</span></span><a href="#l472"></a>
<span id="l473">                <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l473"></a>
<span id="l474">                    <span class="n">onerror</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">islink</span><span class="p">,</span> <span class="n">path</span><span class="p">,</span> <span class="n">sys</span><span class="o">.</span><span class="n">exc_info</span><span class="p">())</span></span><a href="#l474"></a>
<span id="l475">        <span class="k">finally</span><span class="p">:</span></span><a href="#l475"></a>
<span id="l476">            <span class="n">os</span><span class="o">.</span><span class="n">close</span><span class="p">(</span><span class="n">fd</span><span class="p">)</span></span><a href="#l476"></a>
<span id="l477">    <span class="k">else</span><span class="p">:</span></span><a href="#l477"></a>
<span id="l478">        <span class="k">return</span> <span class="n">_rmtree_unsafe</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">onerror</span><span class="p">)</span></span><a href="#l478"></a>
<span id="l479"></span><a href="#l479"></a>
<span id="l480"><span class="c"># Allow introspection of whether or not the hardening against symlink</span></span><a href="#l480"></a>
<span id="l481"><span class="c"># attacks is supported on the current platform</span></span><a href="#l481"></a>
<span id="l482"><span class="n">rmtree</span><span class="o">.</span><span class="n">avoids_symlink_attacks</span> <span class="o">=</span> <span class="n">_use_fd_functions</span></span><a href="#l482"></a>
<span id="l483"></span><a href="#l483"></a>
<span id="l484"><span class="k">def</span> <span class="nf">_basename</span><span class="p">(</span><span class="n">path</span><span class="p">):</span></span><a href="#l484"></a>
<span id="l485">    <span class="c"># A basename() variant which first strips the trailing slash, if present.</span></span><a href="#l485"></a>
<span id="l486">    <span class="c"># Thus we always get the last component of the path, even for directories.</span></span><a href="#l486"></a>
<span id="l487">    <span class="n">sep</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">sep</span> <span class="o">+</span> <span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">altsep</span> <span class="ow">or</span> <span class="s">&#39;&#39;</span><span class="p">)</span></span><a href="#l487"></a>
<span id="l488">    <span class="k">return</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">basename</span><span class="p">(</span><span class="n">path</span><span class="o">.</span><span class="n">rstrip</span><span class="p">(</span><span class="n">sep</span><span class="p">))</span></span><a href="#l488"></a>
<span id="l489"></span><a href="#l489"></a>
<span id="l490"><span class="k">def</span> <span class="nf">move</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">):</span></span><a href="#l490"></a>
<span id="l491">    <span class="sd">&quot;&quot;&quot;Recursively move a file or directory to another location. This is</span></span><a href="#l491"></a>
<span id="l492"><span class="sd">    similar to the Unix &quot;mv&quot; command. Return the file or directory&#39;s</span></span><a href="#l492"></a>
<span id="l493"><span class="sd">    destination.</span></span><a href="#l493"></a>
<span id="l494"></span><a href="#l494"></a>
<span id="l495"><span class="sd">    If the destination is a directory or a symlink to a directory, the source</span></span><a href="#l495"></a>
<span id="l496"><span class="sd">    is moved inside the directory. The destination path must not already</span></span><a href="#l496"></a>
<span id="l497"><span class="sd">    exist.</span></span><a href="#l497"></a>
<span id="l498"></span><a href="#l498"></a>
<span id="l499"><span class="sd">    If the destination already exists but is not a directory, it may be</span></span><a href="#l499"></a>
<span id="l500"><span class="sd">    overwritten depending on os.rename() semantics.</span></span><a href="#l500"></a>
<span id="l501"></span><a href="#l501"></a>
<span id="l502"><span class="sd">    If the destination is on our current filesystem, then rename() is used.</span></span><a href="#l502"></a>
<span id="l503"><span class="sd">    Otherwise, src is copied to the destination and then removed. Symlinks are</span></span><a href="#l503"></a>
<span id="l504"><span class="sd">    recreated under the new name if os.rename() fails because of cross</span></span><a href="#l504"></a>
<span id="l505"><span class="sd">    filesystem renames.</span></span><a href="#l505"></a>
<span id="l506"></span><a href="#l506"></a>
<span id="l507"><span class="sd">    A lot more could be done here...  A look at a mv.c shows a lot of</span></span><a href="#l507"></a>
<span id="l508"><span class="sd">    the issues this implementation glosses over.</span></span><a href="#l508"></a>
<span id="l509"></span><a href="#l509"></a>
<span id="l510"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l510"></a>
<span id="l511">    <span class="n">real_dst</span> <span class="o">=</span> <span class="n">dst</span></span><a href="#l511"></a>
<span id="l512">    <span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">isdir</span><span class="p">(</span><span class="n">dst</span><span class="p">):</span></span><a href="#l512"></a>
<span id="l513">        <span class="k">if</span> <span class="n">_samefile</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">):</span></span><a href="#l513"></a>
<span id="l514">            <span class="c"># We might be on a case insensitive filesystem,</span></span><a href="#l514"></a>
<span id="l515">            <span class="c"># perform the rename anyway.</span></span><a href="#l515"></a>
<span id="l516">            <span class="n">os</span><span class="o">.</span><span class="n">rename</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">)</span></span><a href="#l516"></a>
<span id="l517">            <span class="k">return</span></span><a href="#l517"></a>
<span id="l518"></span><a href="#l518"></a>
<span id="l519">        <span class="n">real_dst</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">dst</span><span class="p">,</span> <span class="n">_basename</span><span class="p">(</span><span class="n">src</span><span class="p">))</span></span><a href="#l519"></a>
<span id="l520">        <span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">exists</span><span class="p">(</span><span class="n">real_dst</span><span class="p">):</span></span><a href="#l520"></a>
<span id="l521">            <span class="k">raise</span> <span class="n">Error</span><span class="p">(</span><span class="s">&quot;Destination path &#39;</span><span class="si">%s</span><span class="s">&#39; already exists&quot;</span> <span class="o">%</span> <span class="n">real_dst</span><span class="p">)</span></span><a href="#l521"></a>
<span id="l522">    <span class="k">try</span><span class="p">:</span></span><a href="#l522"></a>
<span id="l523">        <span class="n">os</span><span class="o">.</span><span class="n">rename</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">real_dst</span><span class="p">)</span></span><a href="#l523"></a>
<span id="l524">    <span class="k">except</span> <span class="ne">OSError</span><span class="p">:</span></span><a href="#l524"></a>
<span id="l525">        <span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">islink</span><span class="p">(</span><span class="n">src</span><span class="p">):</span></span><a href="#l525"></a>
<span id="l526">            <span class="n">linkto</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">readlink</span><span class="p">(</span><span class="n">src</span><span class="p">)</span></span><a href="#l526"></a>
<span id="l527">            <span class="n">os</span><span class="o">.</span><span class="n">symlink</span><span class="p">(</span><span class="n">linkto</span><span class="p">,</span> <span class="n">real_dst</span><span class="p">)</span></span><a href="#l527"></a>
<span id="l528">            <span class="n">os</span><span class="o">.</span><span class="n">unlink</span><span class="p">(</span><span class="n">src</span><span class="p">)</span></span><a href="#l528"></a>
<span id="l529">        <span class="k">elif</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">isdir</span><span class="p">(</span><span class="n">src</span><span class="p">):</span></span><a href="#l529"></a>
<span id="l530">            <span class="k">if</span> <span class="n">_destinsrc</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">):</span></span><a href="#l530"></a>
<span id="l531">                <span class="k">raise</span> <span class="n">Error</span><span class="p">(</span><span class="s">&quot;Cannot move a directory &#39;</span><span class="si">%s</span><span class="s">&#39; into itself &#39;</span><span class="si">%s</span><span class="s">&#39;.&quot;</span> <span class="o">%</span> <span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">))</span></span><a href="#l531"></a>
<span id="l532">            <span class="n">copytree</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">real_dst</span><span class="p">,</span> <span class="n">symlinks</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span></span><a href="#l532"></a>
<span id="l533">            <span class="n">rmtree</span><span class="p">(</span><span class="n">src</span><span class="p">)</span></span><a href="#l533"></a>
<span id="l534">        <span class="k">else</span><span class="p">:</span></span><a href="#l534"></a>
<span id="l535">            <span class="n">copy2</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">real_dst</span><span class="p">)</span></span><a href="#l535"></a>
<span id="l536">            <span class="n">os</span><span class="o">.</span><span class="n">unlink</span><span class="p">(</span><span class="n">src</span><span class="p">)</span></span><a href="#l536"></a>
<span id="l537">    <span class="k">return</span> <span class="n">real_dst</span></span><a href="#l537"></a>
<span id="l538"></span><a href="#l538"></a>
<span id="l539"><span class="k">def</span> <span class="nf">_destinsrc</span><span class="p">(</span><span class="n">src</span><span class="p">,</span> <span class="n">dst</span><span class="p">):</span></span><a href="#l539"></a>
<span id="l540">    <span class="n">src</span> <span class="o">=</span> <span class="n">abspath</span><span class="p">(</span><span class="n">src</span><span class="p">)</span></span><a href="#l540"></a>
<span id="l541">    <span class="n">dst</span> <span class="o">=</span> <span class="n">abspath</span><span class="p">(</span><span class="n">dst</span><span class="p">)</span></span><a href="#l541"></a>
<span id="l542">    <span class="k">if</span> <span class="ow">not</span> <span class="n">src</span><span class="o">.</span><span class="n">endswith</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">sep</span><span class="p">):</span></span><a href="#l542"></a>
<span id="l543">        <span class="n">src</span> <span class="o">+=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">sep</span></span><a href="#l543"></a>
<span id="l544">    <span class="k">if</span> <span class="ow">not</span> <span class="n">dst</span><span class="o">.</span><span class="n">endswith</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">sep</span><span class="p">):</span></span><a href="#l544"></a>
<span id="l545">        <span class="n">dst</span> <span class="o">+=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">sep</span></span><a href="#l545"></a>
<span id="l546">    <span class="k">return</span> <span class="n">dst</span><span class="o">.</span><span class="n">startswith</span><span class="p">(</span><span class="n">src</span><span class="p">)</span></span><a href="#l546"></a>
<span id="l547"></span><a href="#l547"></a>
<span id="l548"><span class="k">def</span> <span class="nf">_get_gid</span><span class="p">(</span><span class="n">name</span><span class="p">):</span></span><a href="#l548"></a>
<span id="l549">    <span class="sd">&quot;&quot;&quot;Returns a gid, given a group name.&quot;&quot;&quot;</span></span><a href="#l549"></a>
<span id="l550">    <span class="k">if</span> <span class="n">getgrnam</span> <span class="ow">is</span> <span class="bp">None</span> <span class="ow">or</span> <span class="n">name</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l550"></a>
<span id="l551">        <span class="k">return</span> <span class="bp">None</span></span><a href="#l551"></a>
<span id="l552">    <span class="k">try</span><span class="p">:</span></span><a href="#l552"></a>
<span id="l553">        <span class="n">result</span> <span class="o">=</span> <span class="n">getgrnam</span><span class="p">(</span><span class="n">name</span><span class="p">)</span></span><a href="#l553"></a>
<span id="l554">    <span class="k">except</span> <span class="ne">KeyError</span><span class="p">:</span></span><a href="#l554"></a>
<span id="l555">        <span class="n">result</span> <span class="o">=</span> <span class="bp">None</span></span><a href="#l555"></a>
<span id="l556">    <span class="k">if</span> <span class="n">result</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l556"></a>
<span id="l557">        <span class="k">return</span> <span class="n">result</span><span class="p">[</span><span class="mi">2</span><span class="p">]</span></span><a href="#l557"></a>
<span id="l558">    <span class="k">return</span> <span class="bp">None</span></span><a href="#l558"></a>
<span id="l559"></span><a href="#l559"></a>
<span id="l560"><span class="k">def</span> <span class="nf">_get_uid</span><span class="p">(</span><span class="n">name</span><span class="p">):</span></span><a href="#l560"></a>
<span id="l561">    <span class="sd">&quot;&quot;&quot;Returns an uid, given a user name.&quot;&quot;&quot;</span></span><a href="#l561"></a>
<span id="l562">    <span class="k">if</span> <span class="n">getpwnam</span> <span class="ow">is</span> <span class="bp">None</span> <span class="ow">or</span> <span class="n">name</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l562"></a>
<span id="l563">        <span class="k">return</span> <span class="bp">None</span></span><a href="#l563"></a>
<span id="l564">    <span class="k">try</span><span class="p">:</span></span><a href="#l564"></a>
<span id="l565">        <span class="n">result</span> <span class="o">=</span> <span class="n">getpwnam</span><span class="p">(</span><span class="n">name</span><span class="p">)</span></span><a href="#l565"></a>
<span id="l566">    <span class="k">except</span> <span class="ne">KeyError</span><span class="p">:</span></span><a href="#l566"></a>
<span id="l567">        <span class="n">result</span> <span class="o">=</span> <span class="bp">None</span></span><a href="#l567"></a>
<span id="l568">    <span class="k">if</span> <span class="n">result</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l568"></a>
<span id="l569">        <span class="k">return</span> <span class="n">result</span><span class="p">[</span><span class="mi">2</span><span class="p">]</span></span><a href="#l569"></a>
<span id="l570">    <span class="k">return</span> <span class="bp">None</span></span><a href="#l570"></a>
<span id="l571"></span><a href="#l571"></a>
<span id="l572"><span class="k">def</span> <span class="nf">_make_tarball</span><span class="p">(</span><span class="n">base_name</span><span class="p">,</span> <span class="n">base_dir</span><span class="p">,</span> <span class="n">compress</span><span class="o">=</span><span class="s">&quot;gzip&quot;</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">dry_run</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span></span><a href="#l572"></a>
<span id="l573">                  <span class="n">owner</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="n">group</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="n">logger</span><span class="o">=</span><span class="bp">None</span><span class="p">):</span></span><a href="#l573"></a>
<span id="l574">    <span class="sd">&quot;&quot;&quot;Create a (possibly compressed) tar file from all the files under</span></span><a href="#l574"></a>
<span id="l575"><span class="sd">    &#39;base_dir&#39;.</span></span><a href="#l575"></a>
<span id="l576"></span><a href="#l576"></a>
<span id="l577"><span class="sd">    &#39;compress&#39; must be &quot;gzip&quot; (the default), &quot;bzip2&quot;, or None.</span></span><a href="#l577"></a>
<span id="l578"></span><a href="#l578"></a>
<span id="l579"><span class="sd">    &#39;owner&#39; and &#39;group&#39; can be used to define an owner and a group for the</span></span><a href="#l579"></a>
<span id="l580"><span class="sd">    archive that is being built. If not provided, the current owner and group</span></span><a href="#l580"></a>
<span id="l581"><span class="sd">    will be used.</span></span><a href="#l581"></a>
<span id="l582"></span><a href="#l582"></a>
<span id="l583"><span class="sd">    The output tar file will be named &#39;base_name&#39; +  &quot;.tar&quot;, possibly plus</span></span><a href="#l583"></a>
<span id="l584"><span class="sd">    the appropriate compression extension (&quot;.gz&quot;, or &quot;.bz2&quot;).</span></span><a href="#l584"></a>
<span id="l585"></span><a href="#l585"></a>
<span id="l586"><span class="sd">    Returns the output filename.</span></span><a href="#l586"></a>
<span id="l587"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l587"></a>
<span id="l588">    <span class="n">tar_compression</span> <span class="o">=</span> <span class="p">{</span><span class="s">&#39;gzip&#39;</span><span class="p">:</span> <span class="s">&#39;gz&#39;</span><span class="p">,</span> <span class="bp">None</span><span class="p">:</span> <span class="s">&#39;&#39;</span><span class="p">}</span></span><a href="#l588"></a>
<span id="l589">    <span class="n">compress_ext</span> <span class="o">=</span> <span class="p">{</span><span class="s">&#39;gzip&#39;</span><span class="p">:</span> <span class="s">&#39;.gz&#39;</span><span class="p">}</span></span><a href="#l589"></a>
<span id="l590"></span><a href="#l590"></a>
<span id="l591">    <span class="k">if</span> <span class="n">_BZ2_SUPPORTED</span><span class="p">:</span></span><a href="#l591"></a>
<span id="l592">        <span class="n">tar_compression</span><span class="p">[</span><span class="s">&#39;bzip2&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s">&#39;bz2&#39;</span></span><a href="#l592"></a>
<span id="l593">        <span class="n">compress_ext</span><span class="p">[</span><span class="s">&#39;bzip2&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s">&#39;.bz2&#39;</span></span><a href="#l593"></a>
<span id="l594"></span><a href="#l594"></a>
<span id="l595">    <span class="c"># flags for compression program, each element of list will be an argument</span></span><a href="#l595"></a>
<span id="l596">    <span class="k">if</span> <span class="n">compress</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span> <span class="ow">and</span> <span class="n">compress</span> <span class="ow">not</span> <span class="ow">in</span> <span class="n">compress_ext</span><span class="p">:</span></span><a href="#l596"></a>
<span id="l597">        <span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="s">&quot;bad value for &#39;compress&#39;, or compression format not &quot;</span></span><a href="#l597"></a>
<span id="l598">                         <span class="s">&quot;supported : {0}&quot;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">compress</span><span class="p">))</span></span><a href="#l598"></a>
<span id="l599"></span><a href="#l599"></a>
<span id="l600">    <span class="n">archive_name</span> <span class="o">=</span> <span class="n">base_name</span> <span class="o">+</span> <span class="s">&#39;.tar&#39;</span> <span class="o">+</span> <span class="n">compress_ext</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="n">compress</span><span class="p">,</span> <span class="s">&#39;&#39;</span><span class="p">)</span></span><a href="#l600"></a>
<span id="l601">    <span class="n">archive_dir</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">dirname</span><span class="p">(</span><span class="n">archive_name</span><span class="p">)</span></span><a href="#l601"></a>
<span id="l602"></span><a href="#l602"></a>
<span id="l603">    <span class="k">if</span> <span class="n">archive_dir</span> <span class="ow">and</span> <span class="ow">not</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">exists</span><span class="p">(</span><span class="n">archive_dir</span><span class="p">):</span></span><a href="#l603"></a>
<span id="l604">        <span class="k">if</span> <span class="n">logger</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l604"></a>
<span id="l605">            <span class="n">logger</span><span class="o">.</span><span class="n">info</span><span class="p">(</span><span class="s">&quot;creating </span><span class="si">%s</span><span class="s">&quot;</span><span class="p">,</span> <span class="n">archive_dir</span><span class="p">)</span></span><a href="#l605"></a>
<span id="l606">        <span class="k">if</span> <span class="ow">not</span> <span class="n">dry_run</span><span class="p">:</span></span><a href="#l606"></a>
<span id="l607">            <span class="n">os</span><span class="o">.</span><span class="n">makedirs</span><span class="p">(</span><span class="n">archive_dir</span><span class="p">)</span></span><a href="#l607"></a>
<span id="l608"></span><a href="#l608"></a>
<span id="l609">    <span class="c"># creating the tarball</span></span><a href="#l609"></a>
<span id="l610">    <span class="k">if</span> <span class="n">logger</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l610"></a>
<span id="l611">        <span class="n">logger</span><span class="o">.</span><span class="n">info</span><span class="p">(</span><span class="s">&#39;Creating tar archive&#39;</span><span class="p">)</span></span><a href="#l611"></a>
<span id="l612"></span><a href="#l612"></a>
<span id="l613">    <span class="n">uid</span> <span class="o">=</span> <span class="n">_get_uid</span><span class="p">(</span><span class="n">owner</span><span class="p">)</span></span><a href="#l613"></a>
<span id="l614">    <span class="n">gid</span> <span class="o">=</span> <span class="n">_get_gid</span><span class="p">(</span><span class="n">group</span><span class="p">)</span></span><a href="#l614"></a>
<span id="l615"></span><a href="#l615"></a>
<span id="l616">    <span class="k">def</span> <span class="nf">_set_uid_gid</span><span class="p">(</span><span class="n">tarinfo</span><span class="p">):</span></span><a href="#l616"></a>
<span id="l617">        <span class="k">if</span> <span class="n">gid</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l617"></a>
<span id="l618">            <span class="n">tarinfo</span><span class="o">.</span><span class="n">gid</span> <span class="o">=</span> <span class="n">gid</span></span><a href="#l618"></a>
<span id="l619">            <span class="n">tarinfo</span><span class="o">.</span><span class="n">gname</span> <span class="o">=</span> <span class="n">group</span></span><a href="#l619"></a>
<span id="l620">        <span class="k">if</span> <span class="n">uid</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l620"></a>
<span id="l621">            <span class="n">tarinfo</span><span class="o">.</span><span class="n">uid</span> <span class="o">=</span> <span class="n">uid</span></span><a href="#l621"></a>
<span id="l622">            <span class="n">tarinfo</span><span class="o">.</span><span class="n">uname</span> <span class="o">=</span> <span class="n">owner</span></span><a href="#l622"></a>
<span id="l623">        <span class="k">return</span> <span class="n">tarinfo</span></span><a href="#l623"></a>
<span id="l624"></span><a href="#l624"></a>
<span id="l625">    <span class="k">if</span> <span class="ow">not</span> <span class="n">dry_run</span><span class="p">:</span></span><a href="#l625"></a>
<span id="l626">        <span class="n">tar</span> <span class="o">=</span> <span class="n">tarfile</span><span class="o">.</span><span class="n">open</span><span class="p">(</span><span class="n">archive_name</span><span class="p">,</span> <span class="s">&#39;w|</span><span class="si">%s</span><span class="s">&#39;</span> <span class="o">%</span> <span class="n">tar_compression</span><span class="p">[</span><span class="n">compress</span><span class="p">])</span></span><a href="#l626"></a>
<span id="l627">        <span class="k">try</span><span class="p">:</span></span><a href="#l627"></a>
<span id="l628">            <span class="n">tar</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">base_dir</span><span class="p">,</span> <span class="nb">filter</span><span class="o">=</span><span class="n">_set_uid_gid</span><span class="p">)</span></span><a href="#l628"></a>
<span id="l629">        <span class="k">finally</span><span class="p">:</span></span><a href="#l629"></a>
<span id="l630">            <span class="n">tar</span><span class="o">.</span><span class="n">close</span><span class="p">()</span></span><a href="#l630"></a>
<span id="l631"></span><a href="#l631"></a>
<span id="l632">    <span class="k">return</span> <span class="n">archive_name</span></span><a href="#l632"></a>
<span id="l633"></span><a href="#l633"></a>
<span id="l634"><span class="k">def</span> <span class="nf">_call_external_zip</span><span class="p">(</span><span class="n">base_dir</span><span class="p">,</span> <span class="n">zip_filename</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="bp">False</span><span class="p">,</span> <span class="n">dry_run</span><span class="o">=</span><span class="bp">False</span><span class="p">):</span></span><a href="#l634"></a>
<span id="l635">    <span class="c"># XXX see if we want to keep an external call here</span></span><a href="#l635"></a>
<span id="l636">    <span class="k">if</span> <span class="n">verbose</span><span class="p">:</span></span><a href="#l636"></a>
<span id="l637">        <span class="n">zipoptions</span> <span class="o">=</span> <span class="s">&quot;-r&quot;</span></span><a href="#l637"></a>
<span id="l638">    <span class="k">else</span><span class="p">:</span></span><a href="#l638"></a>
<span id="l639">        <span class="n">zipoptions</span> <span class="o">=</span> <span class="s">&quot;-rq&quot;</span></span><a href="#l639"></a>
<span id="l640">    <span class="kn">from</span> <span class="nn">distutils.errors</span> <span class="kn">import</span> <span class="n">DistutilsExecError</span></span><a href="#l640"></a>
<span id="l641">    <span class="kn">from</span> <span class="nn">distutils.spawn</span> <span class="kn">import</span> <span class="n">spawn</span></span><a href="#l641"></a>
<span id="l642">    <span class="k">try</span><span class="p">:</span></span><a href="#l642"></a>
<span id="l643">        <span class="n">spawn</span><span class="p">([</span><span class="s">&quot;zip&quot;</span><span class="p">,</span> <span class="n">zipoptions</span><span class="p">,</span> <span class="n">zip_filename</span><span class="p">,</span> <span class="n">base_dir</span><span class="p">],</span> <span class="n">dry_run</span><span class="o">=</span><span class="n">dry_run</span><span class="p">)</span></span><a href="#l643"></a>
<span id="l644">    <span class="k">except</span> <span class="n">DistutilsExecError</span><span class="p">:</span></span><a href="#l644"></a>
<span id="l645">        <span class="c"># XXX really should distinguish between &quot;couldn&#39;t find</span></span><a href="#l645"></a>
<span id="l646">        <span class="c"># external &#39;zip&#39; command&quot; and &quot;zip failed&quot;.</span></span><a href="#l646"></a>
<span id="l647">        <span class="k">raise</span> <span class="n">ExecError</span><span class="p">(</span><span class="s">&quot;unable to create zip file &#39;</span><span class="si">%s</span><span class="s">&#39;: &quot;</span></span><a href="#l647"></a>
<span id="l648">            <span class="s">&quot;could neither import the &#39;zipfile&#39; module nor &quot;</span></span><a href="#l648"></a>
<span id="l649">            <span class="s">&quot;find a standalone zip utility&quot;</span><span class="p">)</span> <span class="o">%</span> <span class="n">zip_filename</span></span><a href="#l649"></a>
<span id="l650"></span><a href="#l650"></a>
<span id="l651"><span class="k">def</span> <span class="nf">_make_zipfile</span><span class="p">(</span><span class="n">base_name</span><span class="p">,</span> <span class="n">base_dir</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">dry_run</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">logger</span><span class="o">=</span><span class="bp">None</span><span class="p">):</span></span><a href="#l651"></a>
<span id="l652">    <span class="sd">&quot;&quot;&quot;Create a zip file from all the files under &#39;base_dir&#39;.</span></span><a href="#l652"></a>
<span id="l653"></span><a href="#l653"></a>
<span id="l654"><span class="sd">    The output zip file will be named &#39;base_name&#39; + &quot;.zip&quot;.  Uses either the</span></span><a href="#l654"></a>
<span id="l655"><span class="sd">    &quot;zipfile&quot; Python module (if available) or the InfoZIP &quot;zip&quot; utility</span></span><a href="#l655"></a>
<span id="l656"><span class="sd">    (if installed and found on the default search path).  If neither tool is</span></span><a href="#l656"></a>
<span id="l657"><span class="sd">    available, raises ExecError.  Returns the name of the output zip</span></span><a href="#l657"></a>
<span id="l658"><span class="sd">    file.</span></span><a href="#l658"></a>
<span id="l659"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l659"></a>
<span id="l660">    <span class="n">zip_filename</span> <span class="o">=</span> <span class="n">base_name</span> <span class="o">+</span> <span class="s">&quot;.zip&quot;</span></span><a href="#l660"></a>
<span id="l661">    <span class="n">archive_dir</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">dirname</span><span class="p">(</span><span class="n">base_name</span><span class="p">)</span></span><a href="#l661"></a>
<span id="l662"></span><a href="#l662"></a>
<span id="l663">    <span class="k">if</span> <span class="n">archive_dir</span> <span class="ow">and</span> <span class="ow">not</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">exists</span><span class="p">(</span><span class="n">archive_dir</span><span class="p">):</span></span><a href="#l663"></a>
<span id="l664">        <span class="k">if</span> <span class="n">logger</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l664"></a>
<span id="l665">            <span class="n">logger</span><span class="o">.</span><span class="n">info</span><span class="p">(</span><span class="s">&quot;creating </span><span class="si">%s</span><span class="s">&quot;</span><span class="p">,</span> <span class="n">archive_dir</span><span class="p">)</span></span><a href="#l665"></a>
<span id="l666">        <span class="k">if</span> <span class="ow">not</span> <span class="n">dry_run</span><span class="p">:</span></span><a href="#l666"></a>
<span id="l667">            <span class="n">os</span><span class="o">.</span><span class="n">makedirs</span><span class="p">(</span><span class="n">archive_dir</span><span class="p">)</span></span><a href="#l667"></a>
<span id="l668"></span><a href="#l668"></a>
<span id="l669">    <span class="c"># If zipfile module is not available, try spawning an external &#39;zip&#39;</span></span><a href="#l669"></a>
<span id="l670">    <span class="c"># command.</span></span><a href="#l670"></a>
<span id="l671">    <span class="k">try</span><span class="p">:</span></span><a href="#l671"></a>
<span id="l672">        <span class="kn">import</span> <span class="nn">zipfile</span></span><a href="#l672"></a>
<span id="l673">    <span class="k">except</span> <span class="ne">ImportError</span><span class="p">:</span></span><a href="#l673"></a>
<span id="l674">        <span class="n">zipfile</span> <span class="o">=</span> <span class="bp">None</span></span><a href="#l674"></a>
<span id="l675"></span><a href="#l675"></a>
<span id="l676">    <span class="k">if</span> <span class="n">zipfile</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l676"></a>
<span id="l677">        <span class="n">_call_external_zip</span><span class="p">(</span><span class="n">base_dir</span><span class="p">,</span> <span class="n">zip_filename</span><span class="p">,</span> <span class="n">verbose</span><span class="p">,</span> <span class="n">dry_run</span><span class="p">)</span></span><a href="#l677"></a>
<span id="l678">    <span class="k">else</span><span class="p">:</span></span><a href="#l678"></a>
<span id="l679">        <span class="k">if</span> <span class="n">logger</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l679"></a>
<span id="l680">            <span class="n">logger</span><span class="o">.</span><span class="n">info</span><span class="p">(</span><span class="s">&quot;creating &#39;</span><span class="si">%s</span><span class="s">&#39; and adding &#39;</span><span class="si">%s</span><span class="s">&#39; to it&quot;</span><span class="p">,</span></span><a href="#l680"></a>
<span id="l681">                        <span class="n">zip_filename</span><span class="p">,</span> <span class="n">base_dir</span><span class="p">)</span></span><a href="#l681"></a>
<span id="l682"></span><a href="#l682"></a>
<span id="l683">        <span class="k">if</span> <span class="ow">not</span> <span class="n">dry_run</span><span class="p">:</span></span><a href="#l683"></a>
<span id="l684">            <span class="k">with</span> <span class="n">zipfile</span><span class="o">.</span><span class="n">ZipFile</span><span class="p">(</span><span class="n">zip_filename</span><span class="p">,</span> <span class="s">&quot;w&quot;</span><span class="p">,</span></span><a href="#l684"></a>
<span id="l685">                                 <span class="n">compression</span><span class="o">=</span><span class="n">zipfile</span><span class="o">.</span><span class="n">ZIP_DEFLATED</span><span class="p">)</span> <span class="k">as</span> <span class="n">zf</span><span class="p">:</span></span><a href="#l685"></a>
<span id="l686">                <span class="k">for</span> <span class="n">dirpath</span><span class="p">,</span> <span class="n">dirnames</span><span class="p">,</span> <span class="n">filenames</span> <span class="ow">in</span> <span class="n">os</span><span class="o">.</span><span class="n">walk</span><span class="p">(</span><span class="n">base_dir</span><span class="p">):</span></span><a href="#l686"></a>
<span id="l687">                    <span class="k">for</span> <span class="n">name</span> <span class="ow">in</span> <span class="n">filenames</span><span class="p">:</span></span><a href="#l687"></a>
<span id="l688">                        <span class="n">path</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">normpath</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">dirpath</span><span class="p">,</span> <span class="n">name</span><span class="p">))</span></span><a href="#l688"></a>
<span id="l689">                        <span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">isfile</span><span class="p">(</span><span class="n">path</span><span class="p">):</span></span><a href="#l689"></a>
<span id="l690">                            <span class="n">zf</span><span class="o">.</span><span class="n">write</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">path</span><span class="p">)</span></span><a href="#l690"></a>
<span id="l691">                            <span class="k">if</span> <span class="n">logger</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l691"></a>
<span id="l692">                                <span class="n">logger</span><span class="o">.</span><span class="n">info</span><span class="p">(</span><span class="s">&quot;adding &#39;</span><span class="si">%s</span><span class="s">&#39;&quot;</span><span class="p">,</span> <span class="n">path</span><span class="p">)</span></span><a href="#l692"></a>
<span id="l693"></span><a href="#l693"></a>
<span id="l694">    <span class="k">return</span> <span class="n">zip_filename</span></span><a href="#l694"></a>
<span id="l695"></span><a href="#l695"></a>
<span id="l696"><span class="n">_ARCHIVE_FORMATS</span> <span class="o">=</span> <span class="p">{</span></span><a href="#l696"></a>
<span id="l697">    <span class="s">&#39;gztar&#39;</span><span class="p">:</span> <span class="p">(</span><span class="n">_make_tarball</span><span class="p">,</span> <span class="p">[(</span><span class="s">&#39;compress&#39;</span><span class="p">,</span> <span class="s">&#39;gzip&#39;</span><span class="p">)],</span> <span class="s">&quot;gzip&#39;ed tar-file&quot;</span><span class="p">),</span></span><a href="#l697"></a>
<span id="l698">    <span class="s">&#39;tar&#39;</span><span class="p">:</span>   <span class="p">(</span><span class="n">_make_tarball</span><span class="p">,</span> <span class="p">[(</span><span class="s">&#39;compress&#39;</span><span class="p">,</span> <span class="bp">None</span><span class="p">)],</span> <span class="s">&quot;uncompressed tar file&quot;</span><span class="p">),</span></span><a href="#l698"></a>
<span id="l699">    <span class="s">&#39;zip&#39;</span><span class="p">:</span>   <span class="p">(</span><span class="n">_make_zipfile</span><span class="p">,</span> <span class="p">[],</span> <span class="s">&quot;ZIP file&quot;</span><span class="p">)</span></span><a href="#l699"></a>
<span id="l700">    <span class="p">}</span></span><a href="#l700"></a>
<span id="l701"></span><a href="#l701"></a>
<span id="l702"><span class="k">if</span> <span class="n">_BZ2_SUPPORTED</span><span class="p">:</span></span><a href="#l702"></a>
<span id="l703">    <span class="n">_ARCHIVE_FORMATS</span><span class="p">[</span><span class="s">&#39;bztar&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">(</span><span class="n">_make_tarball</span><span class="p">,</span> <span class="p">[(</span><span class="s">&#39;compress&#39;</span><span class="p">,</span> <span class="s">&#39;bzip2&#39;</span><span class="p">)],</span></span><a href="#l703"></a>
<span id="l704">                                <span class="s">&quot;bzip2&#39;ed tar-file&quot;</span><span class="p">)</span></span><a href="#l704"></a>
<span id="l705"></span><a href="#l705"></a>
<span id="l706"><span class="k">def</span> <span class="nf">get_archive_formats</span><span class="p">():</span></span><a href="#l706"></a>
<span id="l707">    <span class="sd">&quot;&quot;&quot;Returns a list of supported formats for archiving and unarchiving.</span></span><a href="#l707"></a>
<span id="l708"></span><a href="#l708"></a>
<span id="l709"><span class="sd">    Each element of the returned sequence is a tuple (name, description)</span></span><a href="#l709"></a>
<span id="l710"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l710"></a>
<span id="l711">    <span class="n">formats</span> <span class="o">=</span> <span class="p">[(</span><span class="n">name</span><span class="p">,</span> <span class="n">registry</span><span class="p">[</span><span class="mi">2</span><span class="p">])</span> <span class="k">for</span> <span class="n">name</span><span class="p">,</span> <span class="n">registry</span> <span class="ow">in</span></span><a href="#l711"></a>
<span id="l712">               <span class="n">_ARCHIVE_FORMATS</span><span class="o">.</span><span class="n">items</span><span class="p">()]</span></span><a href="#l712"></a>
<span id="l713">    <span class="n">formats</span><span class="o">.</span><span class="n">sort</span><span class="p">()</span></span><a href="#l713"></a>
<span id="l714">    <span class="k">return</span> <span class="n">formats</span></span><a href="#l714"></a>
<span id="l715"></span><a href="#l715"></a>
<span id="l716"><span class="k">def</span> <span class="nf">register_archive_format</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="n">function</span><span class="p">,</span> <span class="n">extra_args</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="n">description</span><span class="o">=</span><span class="s">&#39;&#39;</span><span class="p">):</span></span><a href="#l716"></a>
<span id="l717">    <span class="sd">&quot;&quot;&quot;Registers an archive format.</span></span><a href="#l717"></a>
<span id="l718"></span><a href="#l718"></a>
<span id="l719"><span class="sd">    name is the name of the format. function is the callable that will be</span></span><a href="#l719"></a>
<span id="l720"><span class="sd">    used to create archives. If provided, extra_args is a sequence of</span></span><a href="#l720"></a>
<span id="l721"><span class="sd">    (name, value) tuples that will be passed as arguments to the callable.</span></span><a href="#l721"></a>
<span id="l722"><span class="sd">    description can be provided to describe the format, and will be returned</span></span><a href="#l722"></a>
<span id="l723"><span class="sd">    by the get_archive_formats() function.</span></span><a href="#l723"></a>
<span id="l724"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l724"></a>
<span id="l725">    <span class="k">if</span> <span class="n">extra_args</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l725"></a>
<span id="l726">        <span class="n">extra_args</span> <span class="o">=</span> <span class="p">[]</span></span><a href="#l726"></a>
<span id="l727">    <span class="k">if</span> <span class="ow">not</span> <span class="nb">callable</span><span class="p">(</span><span class="n">function</span><span class="p">):</span></span><a href="#l727"></a>
<span id="l728">        <span class="k">raise</span> <span class="ne">TypeError</span><span class="p">(</span><span class="s">&#39;The </span><span class="si">%s</span><span class="s"> object is not callable&#39;</span> <span class="o">%</span> <span class="n">function</span><span class="p">)</span></span><a href="#l728"></a>
<span id="l729">    <span class="k">if</span> <span class="ow">not</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">extra_args</span><span class="p">,</span> <span class="p">(</span><span class="nb">tuple</span><span class="p">,</span> <span class="nb">list</span><span class="p">)):</span></span><a href="#l729"></a>
<span id="l730">        <span class="k">raise</span> <span class="ne">TypeError</span><span class="p">(</span><span class="s">&#39;extra_args needs to be a sequence&#39;</span><span class="p">)</span></span><a href="#l730"></a>
<span id="l731">    <span class="k">for</span> <span class="n">element</span> <span class="ow">in</span> <span class="n">extra_args</span><span class="p">:</span></span><a href="#l731"></a>
<span id="l732">        <span class="k">if</span> <span class="ow">not</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">element</span><span class="p">,</span> <span class="p">(</span><span class="nb">tuple</span><span class="p">,</span> <span class="nb">list</span><span class="p">))</span> <span class="ow">or</span> <span class="nb">len</span><span class="p">(</span><span class="n">element</span><span class="p">)</span> <span class="o">!=</span><span class="mi">2</span><span class="p">:</span></span><a href="#l732"></a>
<span id="l733">            <span class="k">raise</span> <span class="ne">TypeError</span><span class="p">(</span><span class="s">&#39;extra_args elements are : (arg_name, value)&#39;</span><span class="p">)</span></span><a href="#l733"></a>
<span id="l734"></span><a href="#l734"></a>
<span id="l735">    <span class="n">_ARCHIVE_FORMATS</span><span class="p">[</span><span class="n">name</span><span class="p">]</span> <span class="o">=</span> <span class="p">(</span><span class="n">function</span><span class="p">,</span> <span class="n">extra_args</span><span class="p">,</span> <span class="n">description</span><span class="p">)</span></span><a href="#l735"></a>
<span id="l736"></span><a href="#l736"></a>
<span id="l737"><span class="k">def</span> <span class="nf">unregister_archive_format</span><span class="p">(</span><span class="n">name</span><span class="p">):</span></span><a href="#l737"></a>
<span id="l738">    <span class="k">del</span> <span class="n">_ARCHIVE_FORMATS</span><span class="p">[</span><span class="n">name</span><span class="p">]</span></span><a href="#l738"></a>
<span id="l739"></span><a href="#l739"></a>
<span id="l740"><span class="k">def</span> <span class="nf">make_archive</span><span class="p">(</span><span class="n">base_name</span><span class="p">,</span> <span class="n">format</span><span class="p">,</span> <span class="n">root_dir</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="n">base_dir</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span></span><a href="#l740"></a>
<span id="l741">                 <span class="n">dry_run</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">owner</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="n">group</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="n">logger</span><span class="o">=</span><span class="bp">None</span><span class="p">):</span></span><a href="#l741"></a>
<span id="l742">    <span class="sd">&quot;&quot;&quot;Create an archive file (eg. zip or tar).</span></span><a href="#l742"></a>
<span id="l743"></span><a href="#l743"></a>
<span id="l744"><span class="sd">    &#39;base_name&#39; is the name of the file to create, minus any format-specific</span></span><a href="#l744"></a>
<span id="l745"><span class="sd">    extension; &#39;format&#39; is the archive format: one of &quot;zip&quot;, &quot;tar&quot;, &quot;bztar&quot;</span></span><a href="#l745"></a>
<span id="l746"><span class="sd">    or &quot;gztar&quot;.</span></span><a href="#l746"></a>
<span id="l747"></span><a href="#l747"></a>
<span id="l748"><span class="sd">    &#39;root_dir&#39; is a directory that will be the root directory of the</span></span><a href="#l748"></a>
<span id="l749"><span class="sd">    archive; ie. we typically chdir into &#39;root_dir&#39; before creating the</span></span><a href="#l749"></a>
<span id="l750"><span class="sd">    archive.  &#39;base_dir&#39; is the directory where we start archiving from;</span></span><a href="#l750"></a>
<span id="l751"><span class="sd">    ie. &#39;base_dir&#39; will be the common prefix of all files and</span></span><a href="#l751"></a>
<span id="l752"><span class="sd">    directories in the archive.  &#39;root_dir&#39; and &#39;base_dir&#39; both default</span></span><a href="#l752"></a>
<span id="l753"><span class="sd">    to the current directory.  Returns the name of the archive file.</span></span><a href="#l753"></a>
<span id="l754"></span><a href="#l754"></a>
<span id="l755"><span class="sd">    &#39;owner&#39; and &#39;group&#39; are used when creating a tar archive. By default,</span></span><a href="#l755"></a>
<span id="l756"><span class="sd">    uses the current owner and group.</span></span><a href="#l756"></a>
<span id="l757"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l757"></a>
<span id="l758">    <span class="n">save_cwd</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getcwd</span><span class="p">()</span></span><a href="#l758"></a>
<span id="l759">    <span class="k">if</span> <span class="n">root_dir</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l759"></a>
<span id="l760">        <span class="k">if</span> <span class="n">logger</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l760"></a>
<span id="l761">            <span class="n">logger</span><span class="o">.</span><span class="n">debug</span><span class="p">(</span><span class="s">&quot;changing into &#39;</span><span class="si">%s</span><span class="s">&#39;&quot;</span><span class="p">,</span> <span class="n">root_dir</span><span class="p">)</span></span><a href="#l761"></a>
<span id="l762">        <span class="n">base_name</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">abspath</span><span class="p">(</span><span class="n">base_name</span><span class="p">)</span></span><a href="#l762"></a>
<span id="l763">        <span class="k">if</span> <span class="ow">not</span> <span class="n">dry_run</span><span class="p">:</span></span><a href="#l763"></a>
<span id="l764">            <span class="n">os</span><span class="o">.</span><span class="n">chdir</span><span class="p">(</span><span class="n">root_dir</span><span class="p">)</span></span><a href="#l764"></a>
<span id="l765"></span><a href="#l765"></a>
<span id="l766">    <span class="k">if</span> <span class="n">base_dir</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l766"></a>
<span id="l767">        <span class="n">base_dir</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">curdir</span></span><a href="#l767"></a>
<span id="l768"></span><a href="#l768"></a>
<span id="l769">    <span class="n">kwargs</span> <span class="o">=</span> <span class="p">{</span><span class="s">&#39;dry_run&#39;</span><span class="p">:</span> <span class="n">dry_run</span><span class="p">,</span> <span class="s">&#39;logger&#39;</span><span class="p">:</span> <span class="n">logger</span><span class="p">}</span></span><a href="#l769"></a>
<span id="l770"></span><a href="#l770"></a>
<span id="l771">    <span class="k">try</span><span class="p">:</span></span><a href="#l771"></a>
<span id="l772">        <span class="n">format_info</span> <span class="o">=</span> <span class="n">_ARCHIVE_FORMATS</span><span class="p">[</span><span class="n">format</span><span class="p">]</span></span><a href="#l772"></a>
<span id="l773">    <span class="k">except</span> <span class="ne">KeyError</span><span class="p">:</span></span><a href="#l773"></a>
<span id="l774">        <span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="s">&quot;unknown archive format &#39;</span><span class="si">%s</span><span class="s">&#39;&quot;</span> <span class="o">%</span> <span class="n">format</span><span class="p">)</span></span><a href="#l774"></a>
<span id="l775"></span><a href="#l775"></a>
<span id="l776">    <span class="n">func</span> <span class="o">=</span> <span class="n">format_info</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span></span><a href="#l776"></a>
<span id="l777">    <span class="k">for</span> <span class="n">arg</span><span class="p">,</span> <span class="n">val</span> <span class="ow">in</span> <span class="n">format_info</span><span class="p">[</span><span class="mi">1</span><span class="p">]:</span></span><a href="#l777"></a>
<span id="l778">        <span class="n">kwargs</span><span class="p">[</span><span class="n">arg</span><span class="p">]</span> <span class="o">=</span> <span class="n">val</span></span><a href="#l778"></a>
<span id="l779"></span><a href="#l779"></a>
<span id="l780">    <span class="k">if</span> <span class="n">format</span> <span class="o">!=</span> <span class="s">&#39;zip&#39;</span><span class="p">:</span></span><a href="#l780"></a>
<span id="l781">        <span class="n">kwargs</span><span class="p">[</span><span class="s">&#39;owner&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">owner</span></span><a href="#l781"></a>
<span id="l782">        <span class="n">kwargs</span><span class="p">[</span><span class="s">&#39;group&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">group</span></span><a href="#l782"></a>
<span id="l783"></span><a href="#l783"></a>
<span id="l784">    <span class="k">try</span><span class="p">:</span></span><a href="#l784"></a>
<span id="l785">        <span class="n">filename</span> <span class="o">=</span> <span class="n">func</span><span class="p">(</span><span class="n">base_name</span><span class="p">,</span> <span class="n">base_dir</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">)</span></span><a href="#l785"></a>
<span id="l786">    <span class="k">finally</span><span class="p">:</span></span><a href="#l786"></a>
<span id="l787">        <span class="k">if</span> <span class="n">root_dir</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l787"></a>
<span id="l788">            <span class="k">if</span> <span class="n">logger</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l788"></a>
<span id="l789">                <span class="n">logger</span><span class="o">.</span><span class="n">debug</span><span class="p">(</span><span class="s">&quot;changing back to &#39;</span><span class="si">%s</span><span class="s">&#39;&quot;</span><span class="p">,</span> <span class="n">save_cwd</span><span class="p">)</span></span><a href="#l789"></a>
<span id="l790">            <span class="n">os</span><span class="o">.</span><span class="n">chdir</span><span class="p">(</span><span class="n">save_cwd</span><span class="p">)</span></span><a href="#l790"></a>
<span id="l791"></span><a href="#l791"></a>
<span id="l792">    <span class="k">return</span> <span class="n">filename</span></span><a href="#l792"></a>
<span id="l793"></span><a href="#l793"></a>
<span id="l794"></span><a href="#l794"></a>
<span id="l795"><span class="k">def</span> <span class="nf">get_unpack_formats</span><span class="p">():</span></span><a href="#l795"></a>
<span id="l796">    <span class="sd">&quot;&quot;&quot;Returns a list of supported formats for unpacking.</span></span><a href="#l796"></a>
<span id="l797"></span><a href="#l797"></a>
<span id="l798"><span class="sd">    Each element of the returned sequence is a tuple</span></span><a href="#l798"></a>
<span id="l799"><span class="sd">    (name, extensions, description)</span></span><a href="#l799"></a>
<span id="l800"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l800"></a>
<span id="l801">    <span class="n">formats</span> <span class="o">=</span> <span class="p">[(</span><span class="n">name</span><span class="p">,</span> <span class="n">info</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="n">info</span><span class="p">[</span><span class="mi">3</span><span class="p">])</span> <span class="k">for</span> <span class="n">name</span><span class="p">,</span> <span class="n">info</span> <span class="ow">in</span></span><a href="#l801"></a>
<span id="l802">               <span class="n">_UNPACK_FORMATS</span><span class="o">.</span><span class="n">items</span><span class="p">()]</span></span><a href="#l802"></a>
<span id="l803">    <span class="n">formats</span><span class="o">.</span><span class="n">sort</span><span class="p">()</span></span><a href="#l803"></a>
<span id="l804">    <span class="k">return</span> <span class="n">formats</span></span><a href="#l804"></a>
<span id="l805"></span><a href="#l805"></a>
<span id="l806"><span class="k">def</span> <span class="nf">_check_unpack_options</span><span class="p">(</span><span class="n">extensions</span><span class="p">,</span> <span class="n">function</span><span class="p">,</span> <span class="n">extra_args</span><span class="p">):</span></span><a href="#l806"></a>
<span id="l807">    <span class="sd">&quot;&quot;&quot;Checks what gets registered as an unpacker.&quot;&quot;&quot;</span></span><a href="#l807"></a>
<span id="l808">    <span class="c"># first make sure no other unpacker is registered for this extension</span></span><a href="#l808"></a>
<span id="l809">    <span class="n">existing_extensions</span> <span class="o">=</span> <span class="p">{}</span></span><a href="#l809"></a>
<span id="l810">    <span class="k">for</span> <span class="n">name</span><span class="p">,</span> <span class="n">info</span> <span class="ow">in</span> <span class="n">_UNPACK_FORMATS</span><span class="o">.</span><span class="n">items</span><span class="p">():</span></span><a href="#l810"></a>
<span id="l811">        <span class="k">for</span> <span class="n">ext</span> <span class="ow">in</span> <span class="n">info</span><span class="p">[</span><span class="mi">0</span><span class="p">]:</span></span><a href="#l811"></a>
<span id="l812">            <span class="n">existing_extensions</span><span class="p">[</span><span class="n">ext</span><span class="p">]</span> <span class="o">=</span> <span class="n">name</span></span><a href="#l812"></a>
<span id="l813"></span><a href="#l813"></a>
<span id="l814">    <span class="k">for</span> <span class="n">extension</span> <span class="ow">in</span> <span class="n">extensions</span><span class="p">:</span></span><a href="#l814"></a>
<span id="l815">        <span class="k">if</span> <span class="n">extension</span> <span class="ow">in</span> <span class="n">existing_extensions</span><span class="p">:</span></span><a href="#l815"></a>
<span id="l816">            <span class="n">msg</span> <span class="o">=</span> <span class="s">&#39;</span><span class="si">%s</span><span class="s"> is already registered for &quot;</span><span class="si">%s</span><span class="s">&quot;&#39;</span></span><a href="#l816"></a>
<span id="l817">            <span class="k">raise</span> <span class="n">RegistryError</span><span class="p">(</span><span class="n">msg</span> <span class="o">%</span> <span class="p">(</span><span class="n">extension</span><span class="p">,</span></span><a href="#l817"></a>
<span id="l818">                                       <span class="n">existing_extensions</span><span class="p">[</span><span class="n">extension</span><span class="p">]))</span></span><a href="#l818"></a>
<span id="l819"></span><a href="#l819"></a>
<span id="l820">    <span class="k">if</span> <span class="ow">not</span> <span class="nb">callable</span><span class="p">(</span><span class="n">function</span><span class="p">):</span></span><a href="#l820"></a>
<span id="l821">        <span class="k">raise</span> <span class="ne">TypeError</span><span class="p">(</span><span class="s">&#39;The registered function must be a callable&#39;</span><span class="p">)</span></span><a href="#l821"></a>
<span id="l822"></span><a href="#l822"></a>
<span id="l823"></span><a href="#l823"></a>
<span id="l824"><span class="k">def</span> <span class="nf">register_unpack_format</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="n">extensions</span><span class="p">,</span> <span class="n">function</span><span class="p">,</span> <span class="n">extra_args</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span></span><a href="#l824"></a>
<span id="l825">                           <span class="n">description</span><span class="o">=</span><span class="s">&#39;&#39;</span><span class="p">):</span></span><a href="#l825"></a>
<span id="l826">    <span class="sd">&quot;&quot;&quot;Registers an unpack format.</span></span><a href="#l826"></a>
<span id="l827"></span><a href="#l827"></a>
<span id="l828"><span class="sd">    `name` is the name of the format. `extensions` is a list of extensions</span></span><a href="#l828"></a>
<span id="l829"><span class="sd">    corresponding to the format.</span></span><a href="#l829"></a>
<span id="l830"></span><a href="#l830"></a>
<span id="l831"><span class="sd">    `function` is the callable that will be</span></span><a href="#l831"></a>
<span id="l832"><span class="sd">    used to unpack archives. The callable will receive archives to unpack.</span></span><a href="#l832"></a>
<span id="l833"><span class="sd">    If it&#39;s unable to handle an archive, it needs to raise a ReadError</span></span><a href="#l833"></a>
<span id="l834"><span class="sd">    exception.</span></span><a href="#l834"></a>
<span id="l835"></span><a href="#l835"></a>
<span id="l836"><span class="sd">    If provided, `extra_args` is a sequence of</span></span><a href="#l836"></a>
<span id="l837"><span class="sd">    (name, value) tuples that will be passed as arguments to the callable.</span></span><a href="#l837"></a>
<span id="l838"><span class="sd">    description can be provided to describe the format, and will be returned</span></span><a href="#l838"></a>
<span id="l839"><span class="sd">    by the get_unpack_formats() function.</span></span><a href="#l839"></a>
<span id="l840"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l840"></a>
<span id="l841">    <span class="k">if</span> <span class="n">extra_args</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l841"></a>
<span id="l842">        <span class="n">extra_args</span> <span class="o">=</span> <span class="p">[]</span></span><a href="#l842"></a>
<span id="l843">    <span class="n">_check_unpack_options</span><span class="p">(</span><span class="n">extensions</span><span class="p">,</span> <span class="n">function</span><span class="p">,</span> <span class="n">extra_args</span><span class="p">)</span></span><a href="#l843"></a>
<span id="l844">    <span class="n">_UNPACK_FORMATS</span><span class="p">[</span><span class="n">name</span><span class="p">]</span> <span class="o">=</span> <span class="n">extensions</span><span class="p">,</span> <span class="n">function</span><span class="p">,</span> <span class="n">extra_args</span><span class="p">,</span> <span class="n">description</span></span><a href="#l844"></a>
<span id="l845"></span><a href="#l845"></a>
<span id="l846"><span class="k">def</span> <span class="nf">unregister_unpack_format</span><span class="p">(</span><span class="n">name</span><span class="p">):</span></span><a href="#l846"></a>
<span id="l847">    <span class="sd">&quot;&quot;&quot;Removes the pack format from the registery.&quot;&quot;&quot;</span></span><a href="#l847"></a>
<span id="l848">    <span class="k">del</span> <span class="n">_UNPACK_FORMATS</span><span class="p">[</span><span class="n">name</span><span class="p">]</span></span><a href="#l848"></a>
<span id="l849"></span><a href="#l849"></a>
<span id="l850"><span class="k">def</span> <span class="nf">_ensure_directory</span><span class="p">(</span><span class="n">path</span><span class="p">):</span></span><a href="#l850"></a>
<span id="l851">    <span class="sd">&quot;&quot;&quot;Ensure that the parent directory of `path` exists&quot;&quot;&quot;</span></span><a href="#l851"></a>
<span id="l852">    <span class="n">dirname</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">dirname</span><span class="p">(</span><span class="n">path</span><span class="p">)</span></span><a href="#l852"></a>
<span id="l853">    <span class="k">if</span> <span class="ow">not</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">isdir</span><span class="p">(</span><span class="n">dirname</span><span class="p">):</span></span><a href="#l853"></a>
<span id="l854">        <span class="n">os</span><span class="o">.</span><span class="n">makedirs</span><span class="p">(</span><span class="n">dirname</span><span class="p">)</span></span><a href="#l854"></a>
<span id="l855"></span><a href="#l855"></a>
<span id="l856"><span class="k">def</span> <span class="nf">_unpack_zipfile</span><span class="p">(</span><span class="n">filename</span><span class="p">,</span> <span class="n">extract_dir</span><span class="p">):</span></span><a href="#l856"></a>
<span id="l857">    <span class="sd">&quot;&quot;&quot;Unpack zip `filename` to `extract_dir`</span></span><a href="#l857"></a>
<span id="l858"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l858"></a>
<span id="l859">    <span class="k">try</span><span class="p">:</span></span><a href="#l859"></a>
<span id="l860">        <span class="kn">import</span> <span class="nn">zipfile</span></span><a href="#l860"></a>
<span id="l861">    <span class="k">except</span> <span class="ne">ImportError</span><span class="p">:</span></span><a href="#l861"></a>
<span id="l862">        <span class="k">raise</span> <span class="n">ReadError</span><span class="p">(</span><span class="s">&#39;zlib not supported, cannot unpack this archive.&#39;</span><span class="p">)</span></span><a href="#l862"></a>
<span id="l863"></span><a href="#l863"></a>
<span id="l864">    <span class="k">if</span> <span class="ow">not</span> <span class="n">zipfile</span><span class="o">.</span><span class="n">is_zipfile</span><span class="p">(</span><span class="n">filename</span><span class="p">):</span></span><a href="#l864"></a>
<span id="l865">        <span class="k">raise</span> <span class="n">ReadError</span><span class="p">(</span><span class="s">&quot;</span><span class="si">%s</span><span class="s"> is not a zip file&quot;</span> <span class="o">%</span> <span class="n">filename</span><span class="p">)</span></span><a href="#l865"></a>
<span id="l866"></span><a href="#l866"></a>
<span id="l867">    <span class="nb">zip</span> <span class="o">=</span> <span class="n">zipfile</span><span class="o">.</span><span class="n">ZipFile</span><span class="p">(</span><span class="n">filename</span><span class="p">)</span></span><a href="#l867"></a>
<span id="l868">    <span class="k">try</span><span class="p">:</span></span><a href="#l868"></a>
<span id="l869">        <span class="k">for</span> <span class="n">info</span> <span class="ow">in</span> <span class="nb">zip</span><span class="o">.</span><span class="n">infolist</span><span class="p">():</span></span><a href="#l869"></a>
<span id="l870">            <span class="n">name</span> <span class="o">=</span> <span class="n">info</span><span class="o">.</span><span class="n">filename</span></span><a href="#l870"></a>
<span id="l871"></span><a href="#l871"></a>
<span id="l872">            <span class="c"># don&#39;t extract absolute paths or ones with .. in them</span></span><a href="#l872"></a>
<span id="l873">            <span class="k">if</span> <span class="n">name</span><span class="o">.</span><span class="n">startswith</span><span class="p">(</span><span class="s">&#39;/&#39;</span><span class="p">)</span> <span class="ow">or</span> <span class="s">&#39;..&#39;</span> <span class="ow">in</span> <span class="n">name</span><span class="p">:</span></span><a href="#l873"></a>
<span id="l874">                <span class="k">continue</span></span><a href="#l874"></a>
<span id="l875"></span><a href="#l875"></a>
<span id="l876">            <span class="n">target</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">extract_dir</span><span class="p">,</span> <span class="o">*</span><span class="n">name</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s">&#39;/&#39;</span><span class="p">))</span></span><a href="#l876"></a>
<span id="l877">            <span class="k">if</span> <span class="ow">not</span> <span class="n">target</span><span class="p">:</span></span><a href="#l877"></a>
<span id="l878">                <span class="k">continue</span></span><a href="#l878"></a>
<span id="l879"></span><a href="#l879"></a>
<span id="l880">            <span class="n">_ensure_directory</span><span class="p">(</span><span class="n">target</span><span class="p">)</span></span><a href="#l880"></a>
<span id="l881">            <span class="k">if</span> <span class="ow">not</span> <span class="n">name</span><span class="o">.</span><span class="n">endswith</span><span class="p">(</span><span class="s">&#39;/&#39;</span><span class="p">):</span></span><a href="#l881"></a>
<span id="l882">                <span class="c"># file</span></span><a href="#l882"></a>
<span id="l883">                <span class="n">data</span> <span class="o">=</span> <span class="nb">zip</span><span class="o">.</span><span class="n">read</span><span class="p">(</span><span class="n">info</span><span class="o">.</span><span class="n">filename</span><span class="p">)</span></span><a href="#l883"></a>
<span id="l884">                <span class="n">f</span> <span class="o">=</span> <span class="nb">open</span><span class="p">(</span><span class="n">target</span><span class="p">,</span> <span class="s">&#39;wb&#39;</span><span class="p">)</span></span><a href="#l884"></a>
<span id="l885">                <span class="k">try</span><span class="p">:</span></span><a href="#l885"></a>
<span id="l886">                    <span class="n">f</span><span class="o">.</span><span class="n">write</span><span class="p">(</span><span class="n">data</span><span class="p">)</span></span><a href="#l886"></a>
<span id="l887">                <span class="k">finally</span><span class="p">:</span></span><a href="#l887"></a>
<span id="l888">                    <span class="n">f</span><span class="o">.</span><span class="n">close</span><span class="p">()</span></span><a href="#l888"></a>
<span id="l889">                    <span class="k">del</span> <span class="n">data</span></span><a href="#l889"></a>
<span id="l890">    <span class="k">finally</span><span class="p">:</span></span><a href="#l890"></a>
<span id="l891">        <span class="nb">zip</span><span class="o">.</span><span class="n">close</span><span class="p">()</span></span><a href="#l891"></a>
<span id="l892"></span><a href="#l892"></a>
<span id="l893"><span class="k">def</span> <span class="nf">_unpack_tarfile</span><span class="p">(</span><span class="n">filename</span><span class="p">,</span> <span class="n">extract_dir</span><span class="p">):</span></span><a href="#l893"></a>
<span id="l894">    <span class="sd">&quot;&quot;&quot;Unpack tar/tar.gz/tar.bz2 `filename` to `extract_dir`</span></span><a href="#l894"></a>
<span id="l895"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l895"></a>
<span id="l896">    <span class="k">try</span><span class="p">:</span></span><a href="#l896"></a>
<span id="l897">        <span class="n">tarobj</span> <span class="o">=</span> <span class="n">tarfile</span><span class="o">.</span><span class="n">open</span><span class="p">(</span><span class="n">filename</span><span class="p">)</span></span><a href="#l897"></a>
<span id="l898">    <span class="k">except</span> <span class="n">tarfile</span><span class="o">.</span><span class="n">TarError</span><span class="p">:</span></span><a href="#l898"></a>
<span id="l899">        <span class="k">raise</span> <span class="n">ReadError</span><span class="p">(</span></span><a href="#l899"></a>
<span id="l900">            <span class="s">&quot;</span><span class="si">%s</span><span class="s"> is not a compressed or uncompressed tar file&quot;</span> <span class="o">%</span> <span class="n">filename</span><span class="p">)</span></span><a href="#l900"></a>
<span id="l901">    <span class="k">try</span><span class="p">:</span></span><a href="#l901"></a>
<span id="l902">        <span class="n">tarobj</span><span class="o">.</span><span class="n">extractall</span><span class="p">(</span><span class="n">extract_dir</span><span class="p">)</span></span><a href="#l902"></a>
<span id="l903">    <span class="k">finally</span><span class="p">:</span></span><a href="#l903"></a>
<span id="l904">        <span class="n">tarobj</span><span class="o">.</span><span class="n">close</span><span class="p">()</span></span><a href="#l904"></a>
<span id="l905"></span><a href="#l905"></a>
<span id="l906"><span class="n">_UNPACK_FORMATS</span> <span class="o">=</span> <span class="p">{</span></span><a href="#l906"></a>
<span id="l907">    <span class="s">&#39;gztar&#39;</span><span class="p">:</span> <span class="p">([</span><span class="s">&#39;.tar.gz&#39;</span><span class="p">,</span> <span class="s">&#39;.tgz&#39;</span><span class="p">],</span> <span class="n">_unpack_tarfile</span><span class="p">,</span> <span class="p">[],</span> <span class="s">&quot;gzip&#39;ed tar-file&quot;</span><span class="p">),</span></span><a href="#l907"></a>
<span id="l908">    <span class="s">&#39;tar&#39;</span><span class="p">:</span>   <span class="p">([</span><span class="s">&#39;.tar&#39;</span><span class="p">],</span> <span class="n">_unpack_tarfile</span><span class="p">,</span> <span class="p">[],</span> <span class="s">&quot;uncompressed tar file&quot;</span><span class="p">),</span></span><a href="#l908"></a>
<span id="l909">    <span class="s">&#39;zip&#39;</span><span class="p">:</span>   <span class="p">([</span><span class="s">&#39;.zip&#39;</span><span class="p">],</span> <span class="n">_unpack_zipfile</span><span class="p">,</span> <span class="p">[],</span> <span class="s">&quot;ZIP file&quot;</span><span class="p">)</span></span><a href="#l909"></a>
<span id="l910">    <span class="p">}</span></span><a href="#l910"></a>
<span id="l911"></span><a href="#l911"></a>
<span id="l912"><span class="k">if</span> <span class="n">_BZ2_SUPPORTED</span><span class="p">:</span></span><a href="#l912"></a>
<span id="l913">    <span class="n">_UNPACK_FORMATS</span><span class="p">[</span><span class="s">&#39;bztar&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">([</span><span class="s">&#39;.bz2&#39;</span><span class="p">],</span> <span class="n">_unpack_tarfile</span><span class="p">,</span> <span class="p">[],</span></span><a href="#l913"></a>
<span id="l914">                                <span class="s">&quot;bzip2&#39;ed tar-file&quot;</span><span class="p">)</span></span><a href="#l914"></a>
<span id="l915"></span><a href="#l915"></a>
<span id="l916"><span class="k">def</span> <span class="nf">_find_unpack_format</span><span class="p">(</span><span class="n">filename</span><span class="p">):</span></span><a href="#l916"></a>
<span id="l917">    <span class="k">for</span> <span class="n">name</span><span class="p">,</span> <span class="n">info</span> <span class="ow">in</span> <span class="n">_UNPACK_FORMATS</span><span class="o">.</span><span class="n">items</span><span class="p">():</span></span><a href="#l917"></a>
<span id="l918">        <span class="k">for</span> <span class="n">extension</span> <span class="ow">in</span> <span class="n">info</span><span class="p">[</span><span class="mi">0</span><span class="p">]:</span></span><a href="#l918"></a>
<span id="l919">            <span class="k">if</span> <span class="n">filename</span><span class="o">.</span><span class="n">endswith</span><span class="p">(</span><span class="n">extension</span><span class="p">):</span></span><a href="#l919"></a>
<span id="l920">                <span class="k">return</span> <span class="n">name</span></span><a href="#l920"></a>
<span id="l921">    <span class="k">return</span> <span class="bp">None</span></span><a href="#l921"></a>
<span id="l922"></span><a href="#l922"></a>
<span id="l923"><span class="k">def</span> <span class="nf">unpack_archive</span><span class="p">(</span><span class="n">filename</span><span class="p">,</span> <span class="n">extract_dir</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="n">format</span><span class="o">=</span><span class="bp">None</span><span class="p">):</span></span><a href="#l923"></a>
<span id="l924">    <span class="sd">&quot;&quot;&quot;Unpack an archive.</span></span><a href="#l924"></a>
<span id="l925"></span><a href="#l925"></a>
<span id="l926"><span class="sd">    `filename` is the name of the archive.</span></span><a href="#l926"></a>
<span id="l927"></span><a href="#l927"></a>
<span id="l928"><span class="sd">    `extract_dir` is the name of the target directory, where the archive</span></span><a href="#l928"></a>
<span id="l929"><span class="sd">    is unpacked. If not provided, the current working directory is used.</span></span><a href="#l929"></a>
<span id="l930"></span><a href="#l930"></a>
<span id="l931"><span class="sd">    `format` is the archive format: one of &quot;zip&quot;, &quot;tar&quot;, or &quot;gztar&quot;. Or any</span></span><a href="#l931"></a>
<span id="l932"><span class="sd">    other registered format. If not provided, unpack_archive will use the</span></span><a href="#l932"></a>
<span id="l933"><span class="sd">    filename extension and see if an unpacker was registered for that</span></span><a href="#l933"></a>
<span id="l934"><span class="sd">    extension.</span></span><a href="#l934"></a>
<span id="l935"></span><a href="#l935"></a>
<span id="l936"><span class="sd">    In case none is found, a ValueError is raised.</span></span><a href="#l936"></a>
<span id="l937"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l937"></a>
<span id="l938">    <span class="k">if</span> <span class="n">extract_dir</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l938"></a>
<span id="l939">        <span class="n">extract_dir</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getcwd</span><span class="p">()</span></span><a href="#l939"></a>
<span id="l940"></span><a href="#l940"></a>
<span id="l941">    <span class="k">if</span> <span class="n">format</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l941"></a>
<span id="l942">        <span class="k">try</span><span class="p">:</span></span><a href="#l942"></a>
<span id="l943">            <span class="n">format_info</span> <span class="o">=</span> <span class="n">_UNPACK_FORMATS</span><span class="p">[</span><span class="n">format</span><span class="p">]</span></span><a href="#l943"></a>
<span id="l944">        <span class="k">except</span> <span class="ne">KeyError</span><span class="p">:</span></span><a href="#l944"></a>
<span id="l945">            <span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="s">&quot;Unknown unpack format &#39;{0}&#39;&quot;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">format</span><span class="p">))</span></span><a href="#l945"></a>
<span id="l946"></span><a href="#l946"></a>
<span id="l947">        <span class="n">func</span> <span class="o">=</span> <span class="n">format_info</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span></span><a href="#l947"></a>
<span id="l948">        <span class="n">func</span><span class="p">(</span><span class="n">filename</span><span class="p">,</span> <span class="n">extract_dir</span><span class="p">,</span> <span class="o">**</span><span class="nb">dict</span><span class="p">(</span><span class="n">format_info</span><span class="p">[</span><span class="mi">2</span><span class="p">]))</span></span><a href="#l948"></a>
<span id="l949">    <span class="k">else</span><span class="p">:</span></span><a href="#l949"></a>
<span id="l950">        <span class="c"># we need to look at the registered unpackers supported extensions</span></span><a href="#l950"></a>
<span id="l951">        <span class="n">format</span> <span class="o">=</span> <span class="n">_find_unpack_format</span><span class="p">(</span><span class="n">filename</span><span class="p">)</span></span><a href="#l951"></a>
<span id="l952">        <span class="k">if</span> <span class="n">format</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l952"></a>
<span id="l953">            <span class="k">raise</span> <span class="n">ReadError</span><span class="p">(</span><span class="s">&quot;Unknown archive format &#39;{0}&#39;&quot;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">filename</span><span class="p">))</span></span><a href="#l953"></a>
<span id="l954"></span><a href="#l954"></a>
<span id="l955">        <span class="n">func</span> <span class="o">=</span> <span class="n">_UNPACK_FORMATS</span><span class="p">[</span><span class="n">format</span><span class="p">][</span><span class="mi">1</span><span class="p">]</span></span><a href="#l955"></a>
<span id="l956">        <span class="n">kwargs</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">(</span><span class="n">_UNPACK_FORMATS</span><span class="p">[</span><span class="n">format</span><span class="p">][</span><span class="mi">2</span><span class="p">])</span></span><a href="#l956"></a>
<span id="l957">        <span class="n">func</span><span class="p">(</span><span class="n">filename</span><span class="p">,</span> <span class="n">extract_dir</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">)</span></span><a href="#l957"></a>
<span id="l958"></span><a href="#l958"></a>
<span id="l959"></span><a href="#l959"></a>
<span id="l960"><span class="k">if</span> <span class="nb">hasattr</span><span class="p">(</span><span class="n">os</span><span class="p">,</span> <span class="s">&#39;statvfs&#39;</span><span class="p">):</span></span><a href="#l960"></a>
<span id="l961"></span><a href="#l961"></a>
<span id="l962">    <span class="n">__all__</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="s">&#39;disk_usage&#39;</span><span class="p">)</span></span><a href="#l962"></a>
<span id="l963">    <span class="n">_ntuple_diskusage</span> <span class="o">=</span> <span class="n">collections</span><span class="o">.</span><span class="n">namedtuple</span><span class="p">(</span><span class="s">&#39;usage&#39;</span><span class="p">,</span> <span class="s">&#39;total used free&#39;</span><span class="p">)</span></span><a href="#l963"></a>
<span id="l964"></span><a href="#l964"></a>
<span id="l965">    <span class="k">def</span> <span class="nf">disk_usage</span><span class="p">(</span><span class="n">path</span><span class="p">):</span></span><a href="#l965"></a>
<span id="l966">        <span class="sd">&quot;&quot;&quot;Return disk usage statistics about the given path.</span></span><a href="#l966"></a>
<span id="l967"></span><a href="#l967"></a>
<span id="l968"><span class="sd">        Returned value is a named tuple with attributes &#39;total&#39;, &#39;used&#39; and</span></span><a href="#l968"></a>
<span id="l969"><span class="sd">        &#39;free&#39;, which are the amount of total, used and free space, in bytes.</span></span><a href="#l969"></a>
<span id="l970"><span class="sd">        &quot;&quot;&quot;</span></span><a href="#l970"></a>
<span id="l971">        <span class="n">st</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">statvfs</span><span class="p">(</span><span class="n">path</span><span class="p">)</span></span><a href="#l971"></a>
<span id="l972">        <span class="n">free</span> <span class="o">=</span> <span class="n">st</span><span class="o">.</span><span class="n">f_bavail</span> <span class="o">*</span> <span class="n">st</span><span class="o">.</span><span class="n">f_frsize</span></span><a href="#l972"></a>
<span id="l973">        <span class="n">total</span> <span class="o">=</span> <span class="n">st</span><span class="o">.</span><span class="n">f_blocks</span> <span class="o">*</span> <span class="n">st</span><span class="o">.</span><span class="n">f_frsize</span></span><a href="#l973"></a>
<span id="l974">        <span class="n">used</span> <span class="o">=</span> <span class="p">(</span><span class="n">st</span><span class="o">.</span><span class="n">f_blocks</span> <span class="o">-</span> <span class="n">st</span><span class="o">.</span><span class="n">f_bfree</span><span class="p">)</span> <span class="o">*</span> <span class="n">st</span><span class="o">.</span><span class="n">f_frsize</span></span><a href="#l974"></a>
<span id="l975">        <span class="k">return</span> <span class="n">_ntuple_diskusage</span><span class="p">(</span><span class="n">total</span><span class="p">,</span> <span class="n">used</span><span class="p">,</span> <span class="n">free</span><span class="p">)</span></span><a href="#l975"></a>
<span id="l976"></span><a href="#l976"></a>
<span id="l977"><span class="k">elif</span> <span class="n">os</span><span class="o">.</span><span class="n">name</span> <span class="o">==</span> <span class="s">&#39;nt&#39;</span><span class="p">:</span></span><a href="#l977"></a>
<span id="l978"></span><a href="#l978"></a>
<span id="l979">    <span class="kn">import</span> <span class="nn">nt</span></span><a href="#l979"></a>
<span id="l980">    <span class="n">__all__</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="s">&#39;disk_usage&#39;</span><span class="p">)</span></span><a href="#l980"></a>
<span id="l981">    <span class="n">_ntuple_diskusage</span> <span class="o">=</span> <span class="n">collections</span><span class="o">.</span><span class="n">namedtuple</span><span class="p">(</span><span class="s">&#39;usage&#39;</span><span class="p">,</span> <span class="s">&#39;total used free&#39;</span><span class="p">)</span></span><a href="#l981"></a>
<span id="l982"></span><a href="#l982"></a>
<span id="l983">    <span class="k">def</span> <span class="nf">disk_usage</span><span class="p">(</span><span class="n">path</span><span class="p">):</span></span><a href="#l983"></a>
<span id="l984">        <span class="sd">&quot;&quot;&quot;Return disk usage statistics about the given path.</span></span><a href="#l984"></a>
<span id="l985"></span><a href="#l985"></a>
<span id="l986"><span class="sd">        Returned values is a named tuple with attributes &#39;total&#39;, &#39;used&#39; and</span></span><a href="#l986"></a>
<span id="l987"><span class="sd">        &#39;free&#39;, which are the amount of total, used and free space, in bytes.</span></span><a href="#l987"></a>
<span id="l988"><span class="sd">        &quot;&quot;&quot;</span></span><a href="#l988"></a>
<span id="l989">        <span class="n">total</span><span class="p">,</span> <span class="n">free</span> <span class="o">=</span> <span class="n">nt</span><span class="o">.</span><span class="n">_getdiskusage</span><span class="p">(</span><span class="n">path</span><span class="p">)</span></span><a href="#l989"></a>
<span id="l990">        <span class="n">used</span> <span class="o">=</span> <span class="n">total</span> <span class="o">-</span> <span class="n">free</span></span><a href="#l990"></a>
<span id="l991">        <span class="k">return</span> <span class="n">_ntuple_diskusage</span><span class="p">(</span><span class="n">total</span><span class="p">,</span> <span class="n">used</span><span class="p">,</span> <span class="n">free</span><span class="p">)</span></span><a href="#l991"></a>
<span id="l992"></span><a href="#l992"></a>
<span id="l993"></span><a href="#l993"></a>
<span id="l994"><span class="k">def</span> <span class="nf">chown</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">user</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="n">group</span><span class="o">=</span><span class="bp">None</span><span class="p">):</span></span><a href="#l994"></a>
<span id="l995">    <span class="sd">&quot;&quot;&quot;Change owner user and group of the given path.</span></span><a href="#l995"></a>
<span id="l996"></span><a href="#l996"></a>
<span id="l997"><span class="sd">    user and group can be the uid/gid or the user/group names, and in that case,</span></span><a href="#l997"></a>
<span id="l998"><span class="sd">    they are converted to their respective uid/gid.</span></span><a href="#l998"></a>
<span id="l999"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l999"></a>
<span id="l1000"></span><a href="#l1000"></a>
<span id="l1001">    <span class="k">if</span> <span class="n">user</span> <span class="ow">is</span> <span class="bp">None</span> <span class="ow">and</span> <span class="n">group</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l1001"></a>
<span id="l1002">        <span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="s">&quot;user and/or group must be set&quot;</span><span class="p">)</span></span><a href="#l1002"></a>
<span id="l1003"></span><a href="#l1003"></a>
<span id="l1004">    <span class="n">_user</span> <span class="o">=</span> <span class="n">user</span></span><a href="#l1004"></a>
<span id="l1005">    <span class="n">_group</span> <span class="o">=</span> <span class="n">group</span></span><a href="#l1005"></a>
<span id="l1006"></span><a href="#l1006"></a>
<span id="l1007">    <span class="c"># -1 means don&#39;t change it</span></span><a href="#l1007"></a>
<span id="l1008">    <span class="k">if</span> <span class="n">user</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l1008"></a>
<span id="l1009">        <span class="n">_user</span> <span class="o">=</span> <span class="o">-</span><span class="mi">1</span></span><a href="#l1009"></a>
<span id="l1010">    <span class="c"># user can either be an int (the uid) or a string (the system username)</span></span><a href="#l1010"></a>
<span id="l1011">    <span class="k">elif</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">user</span><span class="p">,</span> <span class="nb">str</span><span class="p">):</span></span><a href="#l1011"></a>
<span id="l1012">        <span class="n">_user</span> <span class="o">=</span> <span class="n">_get_uid</span><span class="p">(</span><span class="n">user</span><span class="p">)</span></span><a href="#l1012"></a>
<span id="l1013">        <span class="k">if</span> <span class="n">_user</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l1013"></a>
<span id="l1014">            <span class="k">raise</span> <span class="ne">LookupError</span><span class="p">(</span><span class="s">&quot;no such user: {!r}&quot;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">user</span><span class="p">))</span></span><a href="#l1014"></a>
<span id="l1015"></span><a href="#l1015"></a>
<span id="l1016">    <span class="k">if</span> <span class="n">group</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l1016"></a>
<span id="l1017">        <span class="n">_group</span> <span class="o">=</span> <span class="o">-</span><span class="mi">1</span></span><a href="#l1017"></a>
<span id="l1018">    <span class="k">elif</span> <span class="ow">not</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">group</span><span class="p">,</span> <span class="nb">int</span><span class="p">):</span></span><a href="#l1018"></a>
<span id="l1019">        <span class="n">_group</span> <span class="o">=</span> <span class="n">_get_gid</span><span class="p">(</span><span class="n">group</span><span class="p">)</span></span><a href="#l1019"></a>
<span id="l1020">        <span class="k">if</span> <span class="n">_group</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l1020"></a>
<span id="l1021">            <span class="k">raise</span> <span class="ne">LookupError</span><span class="p">(</span><span class="s">&quot;no such group: {!r}&quot;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">group</span><span class="p">))</span></span><a href="#l1021"></a>
<span id="l1022"></span><a href="#l1022"></a>
<span id="l1023">    <span class="n">os</span><span class="o">.</span><span class="n">chown</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">_user</span><span class="p">,</span> <span class="n">_group</span><span class="p">)</span></span><a href="#l1023"></a>
<span id="l1024"></span><a href="#l1024"></a>
<span id="l1025"><span class="k">def</span> <span class="nf">get_terminal_size</span><span class="p">(</span><span class="n">fallback</span><span class="o">=</span><span class="p">(</span><span class="mi">80</span><span class="p">,</span> <span class="mi">24</span><span class="p">)):</span></span><a href="#l1025"></a>
<span id="l1026">    <span class="sd">&quot;&quot;&quot;Get the size of the terminal window.</span></span><a href="#l1026"></a>
<span id="l1027"></span><a href="#l1027"></a>
<span id="l1028"><span class="sd">    For each of the two dimensions, the environment variable, COLUMNS</span></span><a href="#l1028"></a>
<span id="l1029"><span class="sd">    and LINES respectively, is checked. If the variable is defined and</span></span><a href="#l1029"></a>
<span id="l1030"><span class="sd">    the value is a positive integer, it is used.</span></span><a href="#l1030"></a>
<span id="l1031"></span><a href="#l1031"></a>
<span id="l1032"><span class="sd">    When COLUMNS or LINES is not defined, which is the common case,</span></span><a href="#l1032"></a>
<span id="l1033"><span class="sd">    the terminal connected to sys.__stdout__ is queried</span></span><a href="#l1033"></a>
<span id="l1034"><span class="sd">    by invoking os.get_terminal_size.</span></span><a href="#l1034"></a>
<span id="l1035"></span><a href="#l1035"></a>
<span id="l1036"><span class="sd">    If the terminal size cannot be successfully queried, either because</span></span><a href="#l1036"></a>
<span id="l1037"><span class="sd">    the system doesn&#39;t support querying, or because we are not</span></span><a href="#l1037"></a>
<span id="l1038"><span class="sd">    connected to a terminal, the value given in fallback parameter</span></span><a href="#l1038"></a>
<span id="l1039"><span class="sd">    is used. Fallback defaults to (80, 24) which is the default</span></span><a href="#l1039"></a>
<span id="l1040"><span class="sd">    size used by many terminal emulators.</span></span><a href="#l1040"></a>
<span id="l1041"></span><a href="#l1041"></a>
<span id="l1042"><span class="sd">    The value returned is a named tuple of type os.terminal_size.</span></span><a href="#l1042"></a>
<span id="l1043"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l1043"></a>
<span id="l1044">    <span class="c"># columns, lines are the working values</span></span><a href="#l1044"></a>
<span id="l1045">    <span class="k">try</span><span class="p">:</span></span><a href="#l1045"></a>
<span id="l1046">        <span class="n">columns</span> <span class="o">=</span> <span class="nb">int</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">[</span><span class="s">&#39;COLUMNS&#39;</span><span class="p">])</span></span><a href="#l1046"></a>
<span id="l1047">    <span class="k">except</span> <span class="p">(</span><span class="ne">KeyError</span><span class="p">,</span> <span class="ne">ValueError</span><span class="p">):</span></span><a href="#l1047"></a>
<span id="l1048">        <span class="n">columns</span> <span class="o">=</span> <span class="mi">0</span></span><a href="#l1048"></a>
<span id="l1049"></span><a href="#l1049"></a>
<span id="l1050">    <span class="k">try</span><span class="p">:</span></span><a href="#l1050"></a>
<span id="l1051">        <span class="n">lines</span> <span class="o">=</span> <span class="nb">int</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">[</span><span class="s">&#39;LINES&#39;</span><span class="p">])</span></span><a href="#l1051"></a>
<span id="l1052">    <span class="k">except</span> <span class="p">(</span><span class="ne">KeyError</span><span class="p">,</span> <span class="ne">ValueError</span><span class="p">):</span></span><a href="#l1052"></a>
<span id="l1053">        <span class="n">lines</span> <span class="o">=</span> <span class="mi">0</span></span><a href="#l1053"></a>
<span id="l1054"></span><a href="#l1054"></a>
<span id="l1055">    <span class="c"># only query if necessary</span></span><a href="#l1055"></a>
<span id="l1056">    <span class="k">if</span> <span class="n">columns</span> <span class="o">&lt;=</span> <span class="mi">0</span> <span class="ow">or</span> <span class="n">lines</span> <span class="o">&lt;=</span> <span class="mi">0</span><span class="p">:</span></span><a href="#l1056"></a>
<span id="l1057">        <span class="k">try</span><span class="p">:</span></span><a href="#l1057"></a>
<span id="l1058">            <span class="n">size</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">get_terminal_size</span><span class="p">(</span><span class="n">sys</span><span class="o">.</span><span class="n">__stdout__</span><span class="o">.</span><span class="n">fileno</span><span class="p">())</span></span><a href="#l1058"></a>
<span id="l1059">        <span class="k">except</span> <span class="p">(</span><span class="ne">NameError</span><span class="p">,</span> <span class="ne">OSError</span><span class="p">):</span></span><a href="#l1059"></a>
<span id="l1060">            <span class="n">size</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">terminal_size</span><span class="p">(</span><span class="n">fallback</span><span class="p">)</span></span><a href="#l1060"></a>
<span id="l1061">        <span class="k">if</span> <span class="n">columns</span> <span class="o">&lt;=</span> <span class="mi">0</span><span class="p">:</span></span><a href="#l1061"></a>
<span id="l1062">            <span class="n">columns</span> <span class="o">=</span> <span class="n">size</span><span class="o">.</span><span class="n">columns</span></span><a href="#l1062"></a>
<span id="l1063">        <span class="k">if</span> <span class="n">lines</span> <span class="o">&lt;=</span> <span class="mi">0</span><span class="p">:</span></span><a href="#l1063"></a>
<span id="l1064">            <span class="n">lines</span> <span class="o">=</span> <span class="n">size</span><span class="o">.</span><span class="n">lines</span></span><a href="#l1064"></a>
<span id="l1065"></span><a href="#l1065"></a>
<span id="l1066">    <span class="k">return</span> <span class="n">os</span><span class="o">.</span><span class="n">terminal_size</span><span class="p">((</span><span class="n">columns</span><span class="p">,</span> <span class="n">lines</span><span class="p">))</span></span><a href="#l1066"></a>
<span id="l1067"></span><a href="#l1067"></a>
<span id="l1068"><span class="k">def</span> <span class="nf">which</span><span class="p">(</span><span class="n">cmd</span><span class="p">,</span> <span class="n">mode</span><span class="o">=</span><span class="n">os</span><span class="o">.</span><span class="n">F_OK</span> <span class="o">|</span> <span class="n">os</span><span class="o">.</span><span class="n">X_OK</span><span class="p">,</span> <span class="n">path</span><span class="o">=</span><span class="bp">None</span><span class="p">):</span></span><a href="#l1068"></a>
<span id="l1069">    <span class="sd">&quot;&quot;&quot;Given a command, mode, and a PATH string, return the path which</span></span><a href="#l1069"></a>
<span id="l1070"><span class="sd">    conforms to the given mode on the PATH, or None if there is no such</span></span><a href="#l1070"></a>
<span id="l1071"><span class="sd">    file.</span></span><a href="#l1071"></a>
<span id="l1072"></span><a href="#l1072"></a>
<span id="l1073"><span class="sd">    `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result</span></span><a href="#l1073"></a>
<span id="l1074"><span class="sd">    of os.environ.get(&quot;PATH&quot;), or can be overridden with a custom search</span></span><a href="#l1074"></a>
<span id="l1075"><span class="sd">    path.</span></span><a href="#l1075"></a>
<span id="l1076"></span><a href="#l1076"></a>
<span id="l1077"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l1077"></a>
<span id="l1078">    <span class="c"># Check that a given file can be accessed with the correct mode.</span></span><a href="#l1078"></a>
<span id="l1079">    <span class="c"># Additionally check that `file` is not a directory, as on Windows</span></span><a href="#l1079"></a>
<span id="l1080">    <span class="c"># directories pass the os.access check.</span></span><a href="#l1080"></a>
<span id="l1081">    <span class="k">def</span> <span class="nf">_access_check</span><span class="p">(</span><span class="n">fn</span><span class="p">,</span> <span class="n">mode</span><span class="p">):</span></span><a href="#l1081"></a>
<span id="l1082">        <span class="k">return</span> <span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">exists</span><span class="p">(</span><span class="n">fn</span><span class="p">)</span> <span class="ow">and</span> <span class="n">os</span><span class="o">.</span><span class="n">access</span><span class="p">(</span><span class="n">fn</span><span class="p">,</span> <span class="n">mode</span><span class="p">)</span></span><a href="#l1082"></a>
<span id="l1083">                <span class="ow">and</span> <span class="ow">not</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">isdir</span><span class="p">(</span><span class="n">fn</span><span class="p">))</span></span><a href="#l1083"></a>
<span id="l1084"></span><a href="#l1084"></a>
<span id="l1085">    <span class="c"># If we&#39;re given a path with a directory part, look it up directly rather</span></span><a href="#l1085"></a>
<span id="l1086">    <span class="c"># than referring to PATH directories. This includes checking relative to the</span></span><a href="#l1086"></a>
<span id="l1087">    <span class="c"># current directory, e.g. ./script</span></span><a href="#l1087"></a>
<span id="l1088">    <span class="k">if</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">dirname</span><span class="p">(</span><span class="n">cmd</span><span class="p">):</span></span><a href="#l1088"></a>
<span id="l1089">        <span class="k">if</span> <span class="n">_access_check</span><span class="p">(</span><span class="n">cmd</span><span class="p">,</span> <span class="n">mode</span><span class="p">):</span></span><a href="#l1089"></a>
<span id="l1090">            <span class="k">return</span> <span class="n">cmd</span></span><a href="#l1090"></a>
<span id="l1091">        <span class="k">return</span> <span class="bp">None</span></span><a href="#l1091"></a>
<span id="l1092"></span><a href="#l1092"></a>
<span id="l1093">    <span class="k">if</span> <span class="n">path</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l1093"></a>
<span id="l1094">        <span class="n">path</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&quot;PATH&quot;</span><span class="p">,</span> <span class="n">os</span><span class="o">.</span><span class="n">defpath</span><span class="p">)</span></span><a href="#l1094"></a>
<span id="l1095">    <span class="k">if</span> <span class="ow">not</span> <span class="n">path</span><span class="p">:</span></span><a href="#l1095"></a>
<span id="l1096">        <span class="k">return</span> <span class="bp">None</span></span><a href="#l1096"></a>
<span id="l1097">    <span class="n">path</span> <span class="o">=</span> <span class="n">path</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">pathsep</span><span class="p">)</span></span><a href="#l1097"></a>
<span id="l1098"></span><a href="#l1098"></a>
<span id="l1099">    <span class="k">if</span> <span class="n">sys</span><span class="o">.</span><span class="n">platform</span> <span class="o">==</span> <span class="s">&quot;win32&quot;</span><span class="p">:</span></span><a href="#l1099"></a>
<span id="l1100">        <span class="c"># The current directory takes precedence on Windows.</span></span><a href="#l1100"></a>
<span id="l1101">        <span class="k">if</span> <span class="ow">not</span> <span class="n">os</span><span class="o">.</span><span class="n">curdir</span> <span class="ow">in</span> <span class="n">path</span><span class="p">:</span></span><a href="#l1101"></a>
<span id="l1102">            <span class="n">path</span><span class="o">.</span><span class="n">insert</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">os</span><span class="o">.</span><span class="n">curdir</span><span class="p">)</span></span><a href="#l1102"></a>
<span id="l1103"></span><a href="#l1103"></a>
<span id="l1104">        <span class="c"># PATHEXT is necessary to check on Windows.</span></span><a href="#l1104"></a>
<span id="l1105">        <span class="n">pathext</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">&quot;PATHEXT&quot;</span><span class="p">,</span> <span class="s">&quot;&quot;</span><span class="p">)</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">pathsep</span><span class="p">)</span></span><a href="#l1105"></a>
<span id="l1106">        <span class="c"># See if the given file matches any of the expected path extensions.</span></span><a href="#l1106"></a>
<span id="l1107">        <span class="c"># This will allow us to short circuit when given &quot;python.exe&quot;.</span></span><a href="#l1107"></a>
<span id="l1108">        <span class="c"># If it does match, only test that one, otherwise we have to try</span></span><a href="#l1108"></a>
<span id="l1109">        <span class="c"># others.</span></span><a href="#l1109"></a>
<span id="l1110">        <span class="k">if</span> <span class="nb">any</span><span class="p">(</span><span class="n">cmd</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span><span class="o">.</span><span class="n">endswith</span><span class="p">(</span><span class="n">ext</span><span class="o">.</span><span class="n">lower</span><span class="p">())</span> <span class="k">for</span> <span class="n">ext</span> <span class="ow">in</span> <span class="n">pathext</span><span class="p">):</span></span><a href="#l1110"></a>
<span id="l1111">            <span class="n">files</span> <span class="o">=</span> <span class="p">[</span><span class="n">cmd</span><span class="p">]</span></span><a href="#l1111"></a>
<span id="l1112">        <span class="k">else</span><span class="p">:</span></span><a href="#l1112"></a>
<span id="l1113">            <span class="n">files</span> <span class="o">=</span> <span class="p">[</span><span class="n">cmd</span> <span class="o">+</span> <span class="n">ext</span> <span class="k">for</span> <span class="n">ext</span> <span class="ow">in</span> <span class="n">pathext</span><span class="p">]</span></span><a href="#l1113"></a>
<span id="l1114">    <span class="k">else</span><span class="p">:</span></span><a href="#l1114"></a>
<span id="l1115">        <span class="c"># On other platforms you don&#39;t have things like PATHEXT to tell you</span></span><a href="#l1115"></a>
<span id="l1116">        <span class="c"># what file suffixes are executable, so just pass on cmd as-is.</span></span><a href="#l1116"></a>
<span id="l1117">        <span class="n">files</span> <span class="o">=</span> <span class="p">[</span><span class="n">cmd</span><span class="p">]</span></span><a href="#l1117"></a>
<span id="l1118"></span><a href="#l1118"></a>
<span id="l1119">    <span class="n">seen</span> <span class="o">=</span> <span class="nb">set</span><span class="p">()</span></span><a href="#l1119"></a>
<span id="l1120">    <span class="k">for</span> <span class="nb">dir</span> <span class="ow">in</span> <span class="n">path</span><span class="p">:</span></span><a href="#l1120"></a>
<span id="l1121">        <span class="n">normdir</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">normcase</span><span class="p">(</span><span class="nb">dir</span><span class="p">)</span></span><a href="#l1121"></a>
<span id="l1122">        <span class="k">if</span> <span class="ow">not</span> <span class="n">normdir</span> <span class="ow">in</span> <span class="n">seen</span><span class="p">:</span></span><a href="#l1122"></a>
<span id="l1123">            <span class="n">seen</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">normdir</span><span class="p">)</span></span><a href="#l1123"></a>
<span id="l1124">            <span class="k">for</span> <span class="n">thefile</span> <span class="ow">in</span> <span class="n">files</span><span class="p">:</span></span><a href="#l1124"></a>
<span id="l1125">                <span class="n">name</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="nb">dir</span><span class="p">,</span> <span class="n">thefile</span><span class="p">)</span></span><a href="#l1125"></a>
<span id="l1126">                <span class="k">if</span> <span class="n">_access_check</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="n">mode</span><span class="p">):</span></span><a href="#l1126"></a>
<span id="l1127">                    <span class="k">return</span> <span class="n">name</span></span><a href="#l1127"></a>
<span id="l1128">    <span class="k">return</span> <span class="bp">None</span></span><a href="#l1128"></a></pre>
<div class="sourcelast"></div>
</div>
</div>
</div>

<script type="text/javascript">process_dates()</script>


</body>
</html>

