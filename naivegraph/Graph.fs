module Graph

open System.Collections.Generic

type Character = string
type Edges = Dictionary<Character, int>
type CharGraph = Dictionary<Character, Edges>

let addOneToDict (edges: Edges) (character: Character) =
    let weight = 
        match (edges.ContainsKey character) with
        | true -> edges.[character] + 1
        | false -> 1

    edges.[character] <- weight;

let addChar (graph: CharGraph) (scene: Character list) =
    for i in 0 .. scene.Length-1 do
        let c1 = scene.[i]
        
        // if node does not exist, create one
        match graph.ContainsKey c1 with
        | true -> ()
        | false -> graph.[c1] <- new Edges()

        for c2 in scene do
            if c1 <> c2 then
                addOneToDict graph.[c1] c2            