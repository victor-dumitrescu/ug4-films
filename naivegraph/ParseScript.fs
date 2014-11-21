module ParseScript

open FSharp.Data
open System.IO
open Graph

type Script = XmlProvider<"C:/Users/Victor/GitHub/base/Goodfellas/processed/script.xml">

let processScene (scene: XmlProvider<"C:/Users/Victor/GitHub/base/Goodfellas/processed/script.xml">.Scene) =
    [ for speech in scene.Speeches do
          yield speech.Speaker ]
    |> Seq.distinct
    |> List.ofSeq