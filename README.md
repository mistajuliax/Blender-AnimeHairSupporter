Original project for Blender 2.79:

[バグ修正とBlender2.79対応版はこちら](https://github.com/dskjal/Blender-AnimeHairSupporter)  

Updated project for Blender 2.8:

[Blender2.8対応版はこちら](https://github.com/Taremin/Blender-AnimeHairSupporter)  

Translated and fixed project for Blender 2.8:

You're looking at it.

Sceenshot:

![alt text](https://github.com/TheDuriel/Blender-AnimeHairSupporter/blob/master/SS1.jpg)

The plugin panel is on the right 'HairTools'. It allows the automatic adding of taper and bevel curves to Bezier/NURBS curves. In the bottom left you can see the various Taper/Bevel presets.

If you use NURBS curves the Taper/Bevel curves will automatically be aligned with the end of the hair hurve.

Original readme: 

ポリゴン数について：  
これでリアルタイム3D(ゲーム用など)に持ち込む髪を製作するとポリゴン数がとんでもないことになります。  
このアドオンはBlender標準のカーブ機能を使っており、カーブには解像度(分割数)が設定されています、それを見た目が許容できるまで下げてみてください。  
BlenderのDecimate(ポリゴン数削減)モディファイアがなかなか優秀なので、カーブをメッシュ化したあとに使ってみるのも良いかもしれません。  
あとは房ごとにBoolean(ブーリアン、メッシュの統合のこと)を実行しても減るでしょう。  
どの角度からも見えないポリゴンを削除する機能を実装したかったのですが、許容できない計算時間になったので断念しました、自分は手動でやってます。  
