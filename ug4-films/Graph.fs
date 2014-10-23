module Graph

open ApiCalls


type Node = Film * list<Film>
type FilmGraph = Map<Film, Film []>
let maxLevel = 30

let unwrapOption (x: Film [] option) =
    match x with
        | Some fl -> List.ofArray fl
        | None    -> []

let addToExisting (film: Film) (graph: FilmGraph) (elem: Film) =
    //if elem is a member of the graph, add the new edge from elem to film
    if graph.ContainsKey elem then
        let sim = graph.Item elem
        let sim' =
            if Array.exists (fun x -> x = film) sim then
                sim
            else
                Array.append sim [|film|]
        (graph.Remove elem).Add (elem, sim')
    else
        graph


let rec constructGraph (graph: FilmGraph) (queue: Film list) (level: int)=
    if (level = maxLevel) then graph else
        match queue with
        | [] -> graph
        | q ->  match (graph.ContainsKey q.Head) with
                | true -> constructGraph graph q.Tail (level+1)
                | false -> let similar = q.Head.id |> getSimilarFilms
                           match similar with
                           | Some sim -> let (graph': FilmGraph) = Array.fold (addToExisting q.Head) (graph.Add (q.Head, sim)) sim
                                         constructGraph graph' (List.append q.Tail (List.ofArray sim)) (level+1)
                           | None -> constructGraph graph q.Tail (level+1)