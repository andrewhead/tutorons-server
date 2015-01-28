<map version="1.0.1">
<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->
<node CREATED="1421526109693" ID="ID_689353954" MODIFIED="1421793447288" STYLE="fork" TEXT="I came across...">
<node CREATED="1421793448132" ID="ID_364457847" MODIFIED="1421793450831" POSITION="left" TEXT="unclusterd">
<node CREATED="1421794222715" ID="ID_1917026022" MODIFIED="1421794222716" TEXT="----------------&#xa;&#xa;Answer 25837547&#xa;To question 18686860&#xa;&#xa;You&apos;ve received a lot of alternative answers, but just to add another simple solution -- the first thing that came to mind something like this:&#xa;def reverse(text):&#xa;    reversed_text = &quot;&quot;   &#xa;&#xa;    for n in range(len(text)):&#xa;        reversed_text += text[-1 - n]&#xa;&#xa;    return reversed_text&#xa;&#xa;It&apos;s not as fast as some of the other options people have mentioned(or built in methods), but easy to follow as we&apos;re simply using the length of the text string to concatenate one character at a time by slicing from the end toward the front. ">
<node CREATED="1421794290585" ID="ID_408770577" MODIFIED="1421794292692" TEXT="negative indexing"/>
<node CREATED="1421794293337" ID="ID_269848816" MODIFIED="1421794294468" TEXT="iteration"/>
<node CREATED="1421794304297" ID="ID_1031187510" MODIFIED="1421794308564" TEXT="transferring characters"/>
<node CREATED="1421794361976" ID="ID_623096490" MODIFIED="1421794364452" TEXT="assign by operation"/>
<node CREATED="1421794373833" ID="ID_368353170" MODIFIED="1421794381348" TEXT="function"/>
</node>
<node CREATED="1421794239020" ID="ID_1948821008" MODIFIED="1421794239021" TEXT="Answer 24847325&#xa;To question 18686860&#xa;&#xa;I used this:&#xa;def reverse(text):&#xa;s=&quot;&quot;&#xa;l=len(text)&#xa;for i in range(l):&#xa;    s+=text[l-1-i]&#xa;return s">
<node CREATED="1421794367817" ID="ID_1686610171" MODIFIED="1421794385140" TEXT="function"/>
<node CREATED="1421794407865" ID="ID_1907203768" MODIFIED="1421794412116" TEXT="tranferring characters"/>
<node CREATED="1421794412329" ID="ID_684353852" MODIFIED="1421794414004" TEXT="iteration"/>
<node CREATED="1421794421354" ID="ID_1648914507" MODIFIED="1421794424564" TEXT="assign by operation"/>
</node>
<node CREATED="1421794244668" ID="ID_585388260" MODIFIED="1421794244669" TEXT="Answer 24663970&#xa;To question 18686860&#xa;&#xa;Pointfree:&#xa;from functools import partial&#xa;from operator import add&#xa;&#xa;flip = lambda f: lambda x, y: f(y, x)&#xa;rev = partial(reduce, flip(add))&#xa;&#xa;Test:&#xa;&gt;&gt;&gt; rev(&apos;hello&apos;)&#xa;&apos;olleh&apos;"/>
<node CREATED="1421794250572" ID="ID_1423624353" MODIFIED="1421794250573" TEXT="Answer 24663370&#xa;To question 18686860&#xa;&#xa;Only been coding Python for a few days, but I feel like this was a fairly clean solution. Create an empty list, loop through each letter in the string and append it to the front of the list, return the joined list as a string.&#xa;def reverse(text):&#xa;backwardstext = []&#xa;for letter in text:&#xa;    backwardstext.insert(0, letter)&#xa;return &apos;&apos;.join(backwardstext)"/>
<node CREATED="1421794256427" ID="ID_1197331275" MODIFIED="1421794256428" TEXT="Answer 24620050&#xa;To question 18686860&#xa;&#xa;You can simply reverse iterate your string starting from the last character. With python you can use list comprehension to construct the list of characters in reverse order and then join them to get the reversed string in a one-liner:&#xa;def reverse(s):&#xa;  return &quot;&quot;.join([s[-i-1] for i in xrange(len(s))])&#xa;&#xa;if you are not allowed to even use negative indexing you should replace s[-i-1] with s[len(s)-i-1]"/>
<node CREATED="1421794263756" ID="ID_375070086" MODIFIED="1421794263757" TEXT="Answer 18686882&#xa;To question 18686860&#xa;&#xa;You can also do it with recursion:&#xa;def reverse(text):&#xa;    if len(text) &lt;= 1:&#xa;        return text&#xa;&#xa;    return reverse(text[1:]) + text[0]&#xa;&#xa;And a simple example for the string hello:&#xa;   reverse(hello)&#xa; = reverse(ello) + h           # The recursive step&#xa; = reverse(llo) + e + h&#xa; = reverse(lo) + l + e + h&#xa; = reverse(o) + l + l + e + h  # Base case&#xa; = o + l + l + e + h&#xa; = olleh"/>
</node>
<node CREATED="1421794128184" FOLDED="true" ID="ID_378567931" MODIFIED="1421794138474" POSITION="right" TEXT="list operation">
<node CREATED="1421697912363" ID="ID_1669352453" MODIFIED="1421794137182" TEXT="Answer 27994819&#xa;To question 18686860&#xa;&#xa;Here&apos;s my contribution:&#xa;def rev(test):  &#xa;    test = list(test)&#xa;    i = len(test)-1&#xa;    result = []&#xa;&#xa;    print test&#xa;    while i &gt;= 0:&#xa;        result.append(test.pop(i))&#xa;        i -= 1&#xa;    return &quot;&quot;.join(result)">
<node CREATED="1421793569445" ID="ID_299854562" MODIFIED="1421793575216" TEXT="coercing to a list"/>
<node CREATED="1421793585125" ID="ID_1169629409" MODIFIED="1421793588720" TEXT="append-pop workflow"/>
<node CREATED="1421793566213" ID="ID_1899724666" MODIFIED="1421793603072" TEXT="iteration"/>
</node>
</node>
<node CREATED="1421794111144" FOLDED="true" ID="ID_312999436" MODIFIED="1421794389291" POSITION="right" TEXT="transfer char + increment">
<node CREATED="1421793500872" ID="ID_1552881706" MODIFIED="1421794179966" TEXT="Answer 27780382&#xa;To question 18686860&#xa;&#xa;This is my solution using the for i in range loop:&#xa;def reverse(string):&#xa;    tmp = &quot;&quot;&#xa;    for i in range(1,len(string)+1):&#xa;        tmp += string[len(string)-i]            &#xa;    return tmp&#xa;&#xa;It&apos;s pretty easy to understand. I start from 1 to avoid index out of bound.">
<node CREATED="1421793646470" ID="ID_454511057" MODIFIED="1421793647760" TEXT="iteration"/>
<node CREATED="1421793648005" ID="ID_1813393362" MODIFIED="1421793652192" TEXT="transferring characters"/>
<node CREATED="1421793790630" ID="ID_1473834205" MODIFIED="1421793792401" TEXT="string append"/>
</node>
<node CREATED="1421793530776" ID="ID_1516321145" MODIFIED="1421794191743" TEXT="Answer 26665044&#xa;To question 18686860&#xa;&#xa;The way I can think of without using any built-in functions:&#xa;a = &apos;word&apos;&#xa;count = 0&#xa;for letter in a:&#xa;    count += 1&#xa;&#xa;b = &apos;&apos;&#xa;for letter in a:&#xa;    b += a[count-1]&#xa;    count -= 1&#xa;&#xa;And if you print b:&#xa;print b&#xa;drow&#xa;">
<node CREATED="1421793950823" ID="ID_360575817" MODIFIED="1421793953090" TEXT="count by iteration"/>
<node CREATED="1421793946086" ID="ID_622848502" MODIFIED="1421793947986" TEXT="iteration"/>
<node CREATED="1421794076599" ID="ID_1902629731" MODIFIED="1421794080499" TEXT="transferring characters"/>
<node CREATED="1421794105448" ID="ID_941158088" MODIFIED="1421794109523" TEXT="increment operation"/>
<node CREATED="1421794156632" ID="ID_100644917" MODIFIED="1421794158371" TEXT="string append"/>
</node>
<node CREATED="1421793513864" ID="ID_61139214" MODIFIED="1421794202415" TEXT="Answer 27168344&#xa;To question 18686860&#xa;&#xa;def reverseThatString(theString):&#xa;    reversedString = &quot;&quot;&#xa;    lenOfString = len(theString)&#xa;    for i,j in enumerate(theString):&#xa;        lenOfString -= 1&#xa;        reversedString += theString[lenOfString]&#xa;    return reversedString">
<node CREATED="1421793664246" ID="ID_1125763969" MODIFIED="1421793666016" TEXT="enumeration"/>
<node CREATED="1421793779366" ID="ID_1073847997" MODIFIED="1421793781057" TEXT="iteration"/>
<node CREATED="1421793833894" ID="ID_1442404399" MODIFIED="1421793837089" TEXT="increment operation"/>
<node CREATED="1421793992375" ID="ID_586224817" MODIFIED="1421793996498" TEXT="transferring characters"/>
<node CREATED="1421794145911" ID="ID_1762778412" MODIFIED="1421794147651" TEXT="string append"/>
</node>
</node>
<node CREATED="1421794122472" FOLDED="true" ID="ID_1907111584" MODIFIED="1421794207338" POSITION="right" TEXT="transfer char">
<node CREATED="1421698005052" ID="ID_644751095" MODIFIED="1421793481471" TEXT="Answer 27799081&#xa;To question 18686860&#xa;&#xa;You can do simply like this&#xa;def rev(str):&#xa;   rev = &quot;&quot;&#xa;   for i in range(0,len(str)):&#xa;   rev = rev + str[(len(str)-1)-i]&#xa;   print rev">
<node CREATED="1421793599285" ID="ID_405260808" MODIFIED="1421793600560" TEXT="iteration"/>
<node CREATED="1421793612773" ID="ID_1326958956" MODIFIED="1421793629968" TEXT="transferring characters"/>
<node CREATED="1421793786774" ID="ID_1077661975" MODIFIED="1421793788737" TEXT="string append"/>
</node>
<node CREATED="1421793524330" ID="ID_1084722015" MODIFIED="1421794199298" TEXT="Answer 27139401&#xa;To question 18686860&#xa;&#xa;My solution:&#xa;s = raw_input(&quot;Enter string &quot;)&#xa;print&#xa;def reverse(text):  &#xa;st = &quot;&quot;  &#xa;rev = &quot;&quot;  &#xa;count = len(text)  &#xa;print &quot;Lenght of text: &quot;, len(text)  &#xa;print  &#xa;for c in range(len(text)):  &#xa;    count = count - 1  &#xa;    st = st + &quot;&quot;.join(text[c])  &#xa;    rev = rev + &quot;&quot;.join(text[count])  &#xa;    print &quot;count:       &quot;, count  &#xa;    print &quot;print c:     &quot;, c  &#xa;    print &quot;text[c]:     &quot;, text[c]  &#xa;    print  &#xa;print &quot;Original:    &quot;, st  &#xa;print &quot;Reversed:    &quot;, rev  &#xa;return rev  &#xa;&#xa;reverse(s)&#xa;Result screen  &#xa;Enter string  joca  &#xa;Lenght of text:  4  &#xa;count:        3&#xa;print c:      0&#xa;text[c]:      j  &#xa;count:        2&#xa;print c:      1&#xa;text[c]:      o  &#xa;count:        1&#xa;print c:      2&#xa;text[c]:      c  &#xa;count:        0&#xa;print c:      3&#xa;text[c]:      a  &#xa;Original:     joca&#xa;Reversed:     acoj&#xa;None">
<node CREATED="1421793850294" ID="ID_15823497" MODIFIED="1421793919379" TEXT="shows debugging output"/>
<node CREATED="1421793881479" ID="ID_1665593501" MODIFIED="1421793885186" TEXT="character-to-string coercion"/>
<node CREATED="1421793910423" ID="ID_1812733355" MODIFIED="1421793913698" TEXT="forward and backward"/>
<node CREATED="1421794003671" ID="ID_362015239" MODIFIED="1421794006866" TEXT="transferring characters"/>
<node CREATED="1421794151207" ID="ID_84311216" MODIFIED="1421794154099" TEXT="string append"/>
</node>
</node>
</node>
</map>
