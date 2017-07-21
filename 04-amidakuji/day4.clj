(ns day4
    (:require [clojure.string :as str]))

(defstruct link :height :left :right)

; (def network (str/split-lines (slurp "../04-small.txt")))
(def network (str/split-lines (slurp "../04-lines.txt")))

(defn parse-link [l, h]
    (let [endss (rest (str/split l #"\D+"))
          ends (map #(Integer/parseInt %) endss)]
        (struct-map link
            :height h
            :left (first ends)
            :right (second ends))))

(defn parse-network [links]
    (map-indexed 
        (fn [i l] (parse-link l i)) 
        links))

(def parsed-network
    (parse-network network))


(def initial
    (str/split "abcdefghijklmnopqrstuvwxyz" #""))

(defn apply-link [items link]
    (let [li (get link :left)
          ri (get link :right)
          le (nth items li)
          re (nth items ri)
          pre (subvec items 0 li)
          mid (subvec items (inc li) ri)
          suf (subvec items (inc ri))]
    (into [] (concat pre (vector re) mid (vector le) suf))))

(defn follow [items links]
    (reduce apply-link items links))


(defn lane-count [links]
    (inc (apply max (map (fn [l] (get l :right)) links))))

(defn initial-heights [links]
    (vec (replicate (lane-count links) -1)))

(defn pack-one [lane-heights link]
    (let 
        [li (get link :left)
         ri (get link :right)
         new-height (inc (max (nth lane-heights li)
                              (nth lane-heights ri)))]
        (assoc lane-heights li new-height ri new-height)))

(defn pack [lane-heights links]
    (reduce pack-one lane-heights links))


(spit "day4.out" (prn-str 
    (str/join (follow initial parsed-network))))

(spit "day4.out" (prn-str 
    (apply max 
        (pack
            (initial-heights parsed-network)
            parsed-network)))
    :append true)

